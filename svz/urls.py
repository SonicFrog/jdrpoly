from django.contrib.auth.decorators import permission_required
from django.conf.urls import url

from .views import (InfoView, AdminView, PlayerViewSet,
                    PlayerFilterListView)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'json/players', PlayerViewSet)

urlpatterns = [
    url(r'^$', InfoView.as_view(), name='svz-main'),
    url(r'^admin$', permission_required('is_superuser')(AdminView.as_view()),
        name='svz-admin'),
    url(r'^json/find/(?P<name>[\w\s]+)$', PlayerFilterListView.as_view(),
        name='svz-find'),
] + router.urls
