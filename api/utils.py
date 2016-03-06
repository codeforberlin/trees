import sys

from tqdm import tqdm

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.utils.timezone import now

from api.models import Ingest, Tree, History


def ingest_trees_from_file(filename):

    # parse the file (probably gml) with the gdal DataSource class
    data_source = DataSource(filename)

    # create an object in the ingest table
    ingest = Ingest.objects.create(
        filename=filename,
        downloaded_at=now(),
        ingested_at=now()
    )

    # prepare some counters
    counter = {
        'new': 0,
        'updated': 0,
        'skipped': 0
    }

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
                # the properties have changed, we will add the old properties to the history
                history = History(
                    ingest=tree.current_ingest,
                    properties=tree.properties
                )

                # now we can overwrite the current properties
                tree.current_ingest = ingest
                tree.properties = ingest_properties
                tree.save()

                # now we need to save the History object
                history.tree = tree
                history.save()

                counter['updated'] += 1
            else:
                # nothing has changed, we will skip this tree
                counter['skipped'] += 1

        else:
            # this tree has not properties, it must be a new tree
            tree.current_ingest = ingest
            tree.properties = ingest_properties
            tree.save()

            counter['new'] += 1

    return counter
