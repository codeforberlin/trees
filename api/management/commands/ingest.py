from django.core.management.base import BaseCommand

from api.utils import ingest_trees_from_file


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dataset', action='store', help='a short identifier of the dataset')
        parser.add_argument('filename', action='store', help='the gml file')

    def handle(self, *args, **options):

        counter = ingest_trees_from_file(
            options['dataset'],
            options['filename']
        )

        print('new:', counter['new'])
        print('updated:', counter['updated'])
        print('skipped:', counter['skipped'])
