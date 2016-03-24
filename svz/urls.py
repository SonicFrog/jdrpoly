from django.conf.urls import url

from .views import (InfoView, AdminView, PlayerFindView, PlayerViewSet)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'json/players', PlayerViewSet)

urlpatterns = [
    url(r'^$', InfoView.as_view(), name='svz-main'),
    url(r'^admin$', AdminView.as_view(), name='svz-admin'),
    url(r'^json/find/(?P<sciper>\d+)$', PlayerFindView.as_view(), name='svz-find'),
] + router.urls
