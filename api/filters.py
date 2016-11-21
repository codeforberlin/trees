from rest_framework import filters
from rest_framework_gis import filters as gis_filters

from .utils import parse_point


class DistanceToPointFilter(gis_filters.DistanceToPointFilter):

    def get_filter_point(self, request):
        point_string = request.query_params.get(self.point_param, None)
        return parse_point(point_string)


class PropertyFilter(filters.BaseFilterBackend):

    reserved_fields = (
        'dist',
        'point',
        'tile',
        'in_bbox'
    )

    def filter_queryset(self, request, queryset, view):

        query_kwargs = {}
        for key in request.GET:
            if key not in self.reserved_fields:
                field = r'current_propertyset__properties__%s' % key
                query_kwargs[field] = request.GET.get(key)

        return queryset.filter(**query_kwargs)
