from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework_gis.filters import TMSTileFilter, DistanceToPointFilter, InBBoxFilter

from .models import Tree, Attribute
from .serializers import TreeSerializer


class TreePagination(GeoJsonPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class AbstractViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    pagination_class = TreePagination


class ListViewSet(AbstractViewSet):
    pass


class LocationViewSet(AbstractViewSet):

    filter_backends = (DistanceToPointFilter, InBBoxFilter, TMSTileFilter)

    distance_filter_field = 'location'
    bbox_filter_field = 'location'

    bbox_filter_include_overlapping = True
    distance_filter_convert_meters = True


class SearchViewSet(viewsets.ReadOnlyModelViewSet):

    pagination_class = TreePagination

    def list(self, request, format=None):
        tree_ids = self.__tree_ids_from_query_params(request.query_params)
        queryset = Tree.objects.filter(id__in=tree_ids)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer_class = TreeSerializer(paginated_queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def __tree_ids_from_query_params(self, query_params):
        united_tree_ids = {}
        for i, query_param_key in enumerate(query_params.keys()):
            query_param_value = query_params.get(query_param_key, None)
            attribute_queryset = Attribute.objects.filter(key=query_param_key) \
                .filter(Q(string__string_value=query_param_value))
            filtered_tree_ids = {a.tree_id for a in attribute_queryset}
            if i == 0:
                # Init the set
                united_tree_ids = filtered_tree_ids
            else:
                # Intersect both sets (logical AND)
                united_tree_ids = united_tree_ids & filtered_tree_ids
        return united_tree_ids
