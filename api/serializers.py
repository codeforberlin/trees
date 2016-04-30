from rest_framework_gis import serializers

from .models import Tree


class TreeSerializer(serializers.GeoFeatureModelSerializer):

    location = serializers.GeometrySerializerMethodField()

    class Meta:
        model = Tree
        fields = ('id', 'location')
        geo_field = 'location'

    def get_location(self, obj):
        location = obj.location
        location.transform(4326)
        return location

    def get_properties(self, instance, fields):
        return instance.properties
