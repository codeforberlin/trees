from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .models import Tree, PropertySet
from .serializers import TreeSerializer, HistorySerializer
from .filters import PropertyFilter, DistanceToPointFilter


class TreePagination(GeoJsonPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TreeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    pagination_class = TreePagination

    filter_backends = (DistanceToPointFilter, PropertyFilter)

    distance_filter_field = 'location'
    bbox_filter_field = 'location'

    bbox_filter_include_overlapping = True

    @detail_route(methods=['get'])
    def history(self, request, pk):
        history = PropertySet.objects.filter(tree_id=pk).order_by('ingest__downloaded_at')
        return Response(HistorySerializer(history, many=True).data)
