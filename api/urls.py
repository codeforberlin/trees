from django.conf.urls import url, include

from rest_framework import routers

from .views import TreeViewSet, LocationViewSet, SearchViewSet

router = routers.DefaultRouter()
router.register(r'trees', ListViewSet, base_name='tree')
router.register(r'location', LocationViewSet, base_name='location')
router.register(r'search', SearchViewSet, base_name='search')

urlpatterns = [
    url(r'^', include(router.urls)),
]
