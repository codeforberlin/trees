from rest_framework import filters


class PropertyFilter(filters.BaseFilterBackend):
    property_fields = (
        'art_bot',
        'standortnr',
        'spatial_name',
        'kennzeich',
        'kronedurch',
        'bezirk',
        'standalter',
        'stammumfg',
        'baumhoehe',
        'spatial_alias',
        'gml_id',
        'namenr',
        'fid',
        'gattung',
        'spatial_type',
        'pflanzjahr',
        'art_dtsch'
    )

    def filter_queryset(self, request, queryset, view):

        query_kwargs = {}
        for key in request.GET:
            if key in self.property_fields:
                field = r'current_propertyset__properties__%s' % key
                query_kwargs[field] = request.GET.get(key)

        return queryset.filter(**query_kwargs)
