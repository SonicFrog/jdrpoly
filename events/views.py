# coding: utf-8

from django.views.generic import DetailView, ListView
from .models import Event, Edition


class EventListView(ListView):
    template_name = 'events/list.html'
    name = 'event-list'
    context_object_name = 'event_list'
    model = Event


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/view.html'
    context_object_name = 'event'

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetailView, self).get_context_data(*args, **kwargs)
        context['editions'] = kwargs['object'].editions.all()
        context['editions'] = context['editions'].order_by('-date')[:5]
        return context
