from django.conf.urls import url, include

from rest_framework import routers

from .views import TreeViewSet

router = routers.DefaultRouter()
router.register(r'trees', TreeViewSet)
# router.register(r'search', SearchViewSet, base_name='search')


urlpatterns = [
    url(r'^', include(router.urls)),
]
