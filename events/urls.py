from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import (EventListView, EventDetailView, RegisterEditionView,
                    UnregisterEditionView, EditionDetailView, AttendingView,
                    EventPropositionView, CampaignPropositionView,
                    CampaignDetailView, CampaignRegisterView,
                    CampaignUnregisterView)


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
    url(r'^campaign/new$', CampaignPropositionView.as_view(),
        name='propose-campaign'),
    url(r'^campaign/(?P<pk>\d+)$', CampaignDetailView.as_view(),
        name='campaign-detail'),
    url(r'^campaign/(?P<pk>\d+)/enroll$', CampaignRegisterView.as_view(),
        name='campaign-enroll'),
    url(r'^campaign/(?P<pk>\d+)/unenroll$', CampaignUnregisterView,
        name='campaign-unenroll'),
]
