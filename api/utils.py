from collections import Counter
from datetime import datetime
from tqdm import tqdm

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.utils.timezone import now

from api.models import Ingest, Tree, PropertySet


def ingest_trees_from_file(filename, downloaded_at):

    # parse the file (probably gml) with the gdal DataSource class
    data_source = DataSource(filename)

    # parse download date from user input
    downloaded_at_date = datetime.strptime(downloaded_at, '%Y-%m-%dT%H:%MZ')

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
            ingest_properties[key] = feature[key].value

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
