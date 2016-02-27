from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination

from .models import Tree
from .serializers import TreeSerializer


class TreePagination(GeoJsonPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TreeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    pagination_class = TreePagination
