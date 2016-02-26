from django.contrib import admin

from .models import *


class TreeAdmin(admin.ModelAdmin):
    pass


class IngestAdmin(admin.ModelAdmin):
    pass


class StringAdmin(admin.ModelAdmin):
    readonly_fields = ('tree', 'ingest', 'key')
    list_display = ('tree', 'ingest', 'key', 'string_value')
    list_display_links = ('string_value', )


class IntegerAdmin(admin.ModelAdmin):
    readonly_fields = ('tree', 'ingest', 'key')
    list_display = ('tree', 'ingest', 'key', 'integer_value')
    list_display_links = ('integer_value', )


class FloatAdmin(admin.ModelAdmin):
    readonly_fields = ('tree', 'ingest', 'key')
    list_display = ('tree', 'ingest', 'key', 'float_value')
    list_display_links = ('float_value', )


admin.site.register(Tree, TreeAdmin)
admin.site.register(Ingest, IngestAdmin)
admin.site.register(String, StringAdmin)
admin.site.register(Integer, IntegerAdmin)
admin.site.register(Float, FloatAdmin)
