from django.contrib.gis.db import models


class Tree(models.Model):

    location = models.PointField()
    current_ingest = models.ForeignKey('ingest')

    def __str__(self):
        return 'tree_id=%i %s' % (self.pk, str(self.location))

    def get_current_properties(self):
        self.attributes.filter(ingest=self.current_ingest)


class Ingest(models.Model):

    filename = models.CharField(max_length=256)
    downloaded_at = models.DateTimeField(editable=False)
    ingested_at = models.DateTimeField(editable=False)


class Attribute(models.Model):

    tree = models.ForeignKey('Tree', related_name='attributes')

    ingest = models.ForeignKey('ingest')

    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    def __str__(self):
        return 'tree_id=%i %s %s=%s' % (self.tree.pk, self.ingest.ingested_at, self.key, self.value)
