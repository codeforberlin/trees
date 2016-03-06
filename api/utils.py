import sys

from tqdm import tqdm

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.utils.timezone import now

from api.models import Ingest, Tree, AttributeSet


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
            tree = Tree.objects.create(location=point, current_ingest=ingest)

        # create attributes dict for this tree
        ingest_attributes = {}
        for key in feature.fields:
            ingest_attributes[key] = feature[key].value

        # prepare update flag
        update = False

        # get the attributes of the current ingest of the tree
        try:
            current_attributes = AttributeSet.objects.get(tree=tree, ingest=tree.current_ingest).attributes
            if ingest_attributes != current_attributes:
                update = True
                counter['updated'] += 1
        except AttributeSet.DoesNotExist:
            update = True
            counter['new'] += 1

        # update the tree
        if update:
            # update the current_ingest field of the tree
            tree.current_ingest = ingest
            tree.save()

            # create attribute set for this tree and this ingest
            AttributeSet.objects.create(
                tree=tree,
                ingest=ingest,
                attributes=ingest_attributes
            )
        else:
            counter['skipped'] += 1

    return counter
