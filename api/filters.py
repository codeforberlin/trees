from rest_framework import filters


class PropertyFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        query_kwargs = {}
        for key in request.GET:
            field = r'current_propertyset__properties__%s' % key
            query_kwargs[field] = request.GET.get(key)

        return queryset.filter(**query_kwargs)
