from django.contrib import admin

from .models import *


class TreeAdmin(admin.ModelAdmin):
    readonly_fields = ('current_propertyset', )


class IngestAdmin(admin.ModelAdmin):
    pass


class PropertySetAdmin(admin.ModelAdmin):
    readonly_fields = ('tree', 'ingest')

admin.site.register(Tree, TreeAdmin)
admin.site.register(Ingest, IngestAdmin)
admin.site.register(PropertySet, PropertySetAdmin)
