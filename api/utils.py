from tqdm import tqdm

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.utils.timezone import now

from api.models import Tree, Ingest, Attribute


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

        # get the attributes of the current ingest of the tree
        current_attributes = Attribute.objects.filter(tree=tree, ingest=tree.current_ingest).values()

        # prepare update flag
        update = False

        # check if one of the attributes changed
        if current_attributes:
            for attribute in current_attributes:
                if attribute['value'] != unicode(feature.get(attribute['key'])):
                    update = True
                    counter['updated'] += 1
        else:
            update = True
            counter['new'] += 1

        # update the tree
        if update:
            # update the current_ingest field of the tree
            tree.current_ingest = ingest
            tree.save()

            # create attributes for this tree and this ingest
            for key in feature.fields:
                Attribute.objects.create(tree=tree, ingest=ingest, key=key, value=feature.get(key))

        else:
            counter['skipped'] += 1

        print counter
    return counter
