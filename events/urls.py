from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import (EventListView, EventDetailView, RegisterEditionView,
                    UnregisterEditionView, EditionDetailView, AttendingView,
                    EventPropositionView)


urlpatterns = [
    url(r'^$', EventListView.as_view(), name='event-list'),
    url(r'^(?P<pk>\d+)$', EventDetailView.as_view(), name='event-detail'),
    url(r'^edition/(?P<pk>\d+)$', EditionDetailView.as_view(),
        name='edition-detail'),

    url(r'^register/(?P<pk>\d+)$', login_required(RegisterEditionView.as_view()),
        name='edition-register'),
    url(r'^unregister/(?P<pk>\d+)$',
        login_required(UnregisterEditionView.as_view()),
        name='edition-unregister'),

    url(r'^my/$', AttendingView.as_view(), name='my-events'),
    url(r'^propose/$', EventPropositionView.as_view(), name='propose-theme'),
]
