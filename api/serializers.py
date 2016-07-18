from rest_framework import serializers

from rest_framework_gis import serializers as gis_serializers

from .models import Tree, PropertySet


class TreeSerializer(gis_serializers.GeoFeatureModelSerializer):

    location = gis_serializers.GeometrySerializerMethodField()

    class Meta:
        model = Tree
        fields = ('id', 'location')
        geo_field = 'location'

    def get_location(self, obj):
        location = obj.location
        location.transform(4326)
        return location

    def get_properties(self, instance, fields):
        properties = instance.properties
        properties['downloaded_at'] = instance.ingest.downloaded_at
        properties['ingested_at'] = instance.ingest.ingested_at
        return instance.properties


class HistorySerializer(gis_serializers.GeoFeatureModelSerializer):

    id = serializers.IntegerField(source='tree.id')
    location = gis_serializers.GeometrySerializerMethodField()

    class Meta:
        model = PropertySet
        fields = ('id', 'location')
        geo_field = 'location'

    def get_location(self, obj):
        location = obj.tree.location
        location.transform(4326)
        return location

    def get_properties(self, instance, fields):
        properties = instance.properties
        properties['downloaded_at'] = instance.ingest.downloaded_at
        properties['ingested_at'] = instance.ingest.ingested_at
        return instance.properties
