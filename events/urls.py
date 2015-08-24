from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EventListView.as_view(), name='event-list'),

    url(r'^new', views.EventCreateView.as_view(), name='event-create'),

    url(r'^(?P<pk>\d+)$', views.EventParticipateView.as_view(),
        name='event-detail'),

    url(r'^(?P<pk>\d+)/delete$', views.EventDeleteView.as_view(),
        name='event-delete'),

    url(r'^myevents$', views.MyEventsListView.as_view(),
        name='event-list-mine'),

    url(r'^myevents/(?P<pk>\d+)$', views.MyEventDetailView.as_view(),
        name='event-detail-mine')
]
