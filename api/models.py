from django.contrib.gis.db import models


class Tree(models.Model):

    location = models.PointField()
    current_ingest = models.ForeignKey('ingest', blank=True, null=True, on_delete=models.SET_NULL)

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

    key = models.SlugField(max_length=256)

    @property
    def value(self):
        if hasattr(self, 'string'):
            return self.string.string_value
        elif hasattr(self, 'integer'):
            return self.integer.integer_value
        elif hasattr(self, 'float'):
            return self.float.float_value
        else:
            raise Exception('Unknown value class.')

    def __str__(self):
        return 'tree_id=%i ingest=%s key=%s' % (self.tree.pk, self.ingest.ingested_at, self.key)


class String(Attribute):

    string_value = models.CharField(max_length=256)


class Float(Attribute):

    float_value = models.FloatField(blank=True, null=True)


class Integer(Attribute):

    integer_value = models.IntegerField(blank=True, null=True)
