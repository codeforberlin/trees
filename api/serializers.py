from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Tree, Attribute


class TreeSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Tree
        fields = ('id', 'location')
        geo_field = 'location'

    def get_properties(self, instance, fields):
        return instance.get_current_properties()
