from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework_gis.filters import TMSTileFilter, DistanceToPointFilter, InBBoxFilter

from .models import Tree
from .serializers import TreeSerializer
from .filters import PropertyFilter


class TreePagination(GeoJsonPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TreeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    pagination_class = TreePagination

    filter_backends = (DistanceToPointFilter, InBBoxFilter, TMSTileFilter, PropertyFilter)

    distance_filter_field = 'location'
    bbox_filter_field = 'location'

    bbox_filter_include_overlapping = True
    distance_filter_convert_meters = True
