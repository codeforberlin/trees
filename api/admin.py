from django.contrib import admin

from .models import *


class TreeAdmin(admin.ModelAdmin):
    pass


class IngestAdmin(admin.ModelAdmin):
    pass


class AttributeSetAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tree, TreeAdmin)
admin.site.register(Ingest, IngestAdmin)
admin.site.register(AttributeSet, AttributeSetAdmin)