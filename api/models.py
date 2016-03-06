from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

class Tree(models.Model):

    location = models.PointField()
    current_ingest = models.ForeignKey('ingest', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'tree_id=%i %s' % (self.pk, str(self.location))

    # def get_current_properties(self):
    #     return {attribute.key: attribute.value for attribute in self.attributes.filter(ingest=self.current_ingest)}


class Ingest(models.Model):

    filename = models.CharField(max_length=256)
    downloaded_at = models.DateTimeField(editable=False)
    ingested_at = models.DateTimeField(editable=False)


class AttributeSet(models.Model):

    tree = models.ForeignKey('Tree', related_name='attributesets')

    ingest = models.ForeignKey('ingest')

    attributes = JSONField()

    def __str__(self):
        return 'tree_id=%i ingest=%s' % (self.tree.pk, self.ingest.ingested_at)
