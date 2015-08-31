# coding: utf-8

from django.views.generic import (CreateView, ListView, DeleteView, FormView,
                                  DetailView, UpdateView)
from django.core.urlresolvers import reverse_lazy

from .models import Event
from .forms import EventParticipationForm, EventCreationForm
from members.views import LoginRequiredMixin


class EventListView(ListView, LoginRequiredMixin):
    template_name = 'events/list.html'
    name = 'event-list'
    context_object_name = 'event_list'
    model = Event

    def get_queryset(self):
        return Event.objects.order_by('-datetime')[:10]


class EventListByDateView(EventListView):
    pass


class EventListByOwnerView(EventListView):
    def get_queryset(self):
        return Event.objects.order_by('-owner')[:10]


class EventListByPlaceView(EventListView):
    def get_queryset(self):
        return Event.objects.order_by('-place')[:10]


class EventParticipateView(FormView, LoginRequiredMixin):
    form_class = EventParticipationForm
    name = 'event-detail'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class EventUpdateView(UpdateView):
    model = Event
    success_url = reverse_lazy('event-list')


class EventCreateView(CreateView, LoginRequiredMixin):
    model = Event
    success_url = reverse_lazy('event-list')
    name = 'event-new'
    form_class = EventCreationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(EventCreateView, self).form_valid(form)


class EventDeleteView(DeleteView, LoginRequiredMixin):
    model = Event
    success_url = reverse_lazy('event-list')


class MyEventsListView(ListView, LoginRequiredMixin):
    model = Event
    name = 'my-events'

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)

    def get_context_data(self):
        context = super(MyEventsListView, self).get_context_data()
        context['event_type'] = 'Mes évenements'
        return context


class MyEventDetailView(DetailView, LoginRequiredMixin):
    model = Event
    name = 'my-event-single'
