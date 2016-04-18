# coding: utf-8

from django.contrib.auth.decorators import permission_required
from django.conf.urls import url

from .views import (InfoView, AdminView, PlayerViewSet, RankingView,
                    PlayerFilterListView, SendMailView, ProgressView)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'json/players', PlayerViewSet)

urlpatterns = [
    url(r'^$', InfoView.as_view(), name='svz-main'),
    url(r'^admin$', permission_required('is_superuser')(AdminView.as_view()),
        name='svz-admin'),
    url(r'^json/find/(?P<name>[\w\s]+)$', PlayerFilterListView.as_view(),
        name='svz-find'),
    url(r'^json/mail$',
        permission_required('is_superuser')(SendMailView.as_view()),
        name='svz-mail'),
    url(r'^json/rankings$',
        permission_required('is_superuser')(RankingView.as_view()), name='svz-ranking'),
    url(r'^json/status$',
        permission_required('îs_superuser')(ProgressView.as_view()), name='svz-progress'),
] + router.urls
