from django.conf.urls import url
from .views import (EventListView, EventDetailView, RegisterEditionView,
                    UnregisterEditionView, EditionDetailView)

urlpatterns = [
    url(r'^$', EventListView.as_view(), name='event-list'),
    url(r'^(?P<pk>\d+)$', EventDetailView.as_view(), name='event-detail'),
    url(r'^edition/(?P<pk>\d+)$', EditionDetailView.as_view(),
        name='edition-detail'),

    url(r'^register/(?P<pk>\d+)$', RegisterEditionView.as_view(),
        name='edition-register'),
    url(r'^unregister/(?P<pk>\d+)$', UnregisterEditionView.as_view(),
        name='edition-unregister')
]
