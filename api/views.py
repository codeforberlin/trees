from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Tree, PropertySet
from .serializers import TreeSerializer, HistorySerializer
from .filters import PropertyFilter, DistanceToPointFilter
from .utils import parse_point


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

    @list_route(methods=['get'])
    def closest(self, request):
        distance = 1000

        point_string = request.query_params.get('point', None)
        if not point_string:
            raise ValidationError({'point': 'The point need to be provided in the form \'?point=lon,lat\''})

        point = parse_point(point_string)
        tree = Tree.objects.filter(location__distance_lte=(point, D(m=distance))).annotate(distance=Distance('location', point)).order_by('distance').first()
        return Response(TreeSerializer(tree).data)

    @detail_route(methods=['get'])
    def history(self, request, pk):
        history = PropertySet.objects.filter(tree_id=pk).order_by('ingest__downloaded_at')
        return Response(HistorySerializer(history, many=True).data)
