import sys
from tqdm import tqdm

from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from django.utils.timezone import now

from api.models import Tree, Dataset, Property


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename', action='store', help='the gml file')

    def handle(self, *args, **options):
        data_source = DataSource(options['filename'])

        ingest = Ingest.objects.create(
            filename=options['filename'],
            downloaded_at=now(),
            ingested_at=now()
        )

        n = 0
        n_skipped = 0
        for feature in tqdm(data_source[0]):

            point = GEOSGeometry(str(feature.geom), srid=25833)

            try:
                tree = Tree.objects.get(location=point)
            except Tree.DoesNotExist:
                tree = Tree.objects.create(location=point, current_ingest=ingest)

            current_attributes = tree.get_current_attributes()

            attributes = {}
            for key in feature.fields:
                attributes[key] = {
                    'value': feature.get(key),
                    'type': feature.type_name(key)
                }

            # if current_attributes != attributes or new:
            # ingest new attributes 



            sys.exit()

        print('ingested:', n_skipped)
        print('skipped:', n_skipped)
