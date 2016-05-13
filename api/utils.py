import csv

from collections import Counter
from tqdm import tqdm
from dateutil.parser import parse as dateutil_parse

from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.utils.timezone import now

from api.models import Ingest, Tree, PropertySet


def ingest_trees_from_file(filename, downloaded_at):

    if settings.COLUMN_NAMES_CSV:
        column_names = _parse_column_names_csv()
    else:
        column_names = {}

    # parse the file (probably gml) with the gdal DataSource class
    data_source = DataSource(filename)

    # parse download date from user input
    downloaded_at_date = dateutil_parse(downloaded_at)

    # create an object in the ingest table
    ingest = Ingest.objects.create(
        filename=filename,
        downloaded_at=downloaded_at_date,
        ingested_at=now()
    )

    # prepare counter
    counter = Counter()

    # loop over features in the data source (i.e. the trees)
    for feature in tqdm(data_source[0]):
        # parse the point from the point in the feature
        point = GEOSGeometry(str(feature.geom), srid=25833)

        # try to get the tree with the same location or create a new one
        try:
            tree = Tree.objects.get(location=point)
        except Tree.DoesNotExist:
            tree = Tree(location=point)

        # create attributes dict for this tree
        ingest_properties = {}
        for key in feature.fields:
            if key in column_names:
                column_name = column_names[key]
            else:
                column_name = key

            ingest_properties[column_name] = feature[key].value

        if tree.properties:
            if ingest_properties != tree.properties:
                # the properties have changed, we will add the new properties to the history
                propertyset = PropertySet.objects.create(
                    tree=tree,
                    ingest=ingest,
                    properties=ingest_properties
                )

                # now we need to update the tree for the current_propertyset
                tree.current_propertyset = propertyset
                tree.save()

                counter['updated'] += 1
            else:
                # nothing has changed, we will skip this tree
                counter['skipped'] += 1

        else:
            # this tree has no properties, it must be a new tree
            # first we need to save the tree
            tree.save()

            # then we store the properties
            propertyset = PropertySet.objects.create(
                tree=tree,
                ingest=ingest,
                properties=ingest_properties
            )

            # now we need to update the tree for the current_propertyset
            tree.current_propertyset = propertyset
            tree.save()

            counter['new'] += 1

    return counter


def _parse_column_names_csv():
    column_names = {}
    with open(settings.COLUMN_NAMES_CSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            if row:
                for column_name in row[1].split(';'):
                    if column_name:
                        column_names[column_name] = row[0]

    return column_names
