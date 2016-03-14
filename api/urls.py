from django.conf.urls import url, include

from rest_framework import routers

from .views import TreeViewSet, SearchViewSet

router = routers.DefaultRouter()
router.register(r'trees', TreeViewSet, base_name='tree')
router.register(r'search', SearchViewSet, base_name='search')

urlpatterns = [
    url(r'^', include(router.urls)),
]
