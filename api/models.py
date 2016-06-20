from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField


class Tree(models.Model):

    location = models.PointField(srid=25833)
    current_propertyset = models.ForeignKey('PropertySet', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    def __str__(self):
        return 'tree_id=%i %s' % (self.pk, str(self.location))

    @property
    def properties(self):
        if self.current_propertyset:
            return self.current_propertyset.properties
        else:
            return None


class Ingest(models.Model):

    dataset = models.SlugField(null=True)
    filename = models.CharField(max_length=256)
    downloaded_at = models.DateTimeField(editable=False)
    ingested_at = models.DateTimeField(editable=False)


class PropertySet(models.Model):

    tree = models.ForeignKey('Tree', related_name='propertysets')
    ingest = models.ForeignKey('ingest')
    properties = JSONField(blank=True, null=True)

    def __str__(self):
        return 'tree_id=%i ingest=%s' % (self.tree.pk, self.ingest.ingested_at)
