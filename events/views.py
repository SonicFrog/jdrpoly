# coding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect
from django.forms import Form, CharField, Textarea, TextInput
from django.views.generic import DetailView, ListView, UpdateView, FormView
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import Event, Edition
from members.views import LoginRequiredMixin


def redirect_to_edition(pk):
    return HttpResponseRedirect(reverse_lazy('edition-detail',
                                             kwargs={'pk': pk}))


class EventPropositionForm(Form):
    name = CharField(max_length=100,
                     widget=TextInput(attrs={'placeholder': _('Nom')}))
    description = CharField(widget=Textarea(attrs={'placeholder':
                                                   _('Description')}))

    def __init__(self, user):
        self.user = user

    def is_valid(self):
        if not super(EventPropositionForm, self).is_valid():
            return False
        return self.user.profile.is_member()


class EventPropositionView(FormView, LoginRequiredMixin):
    form_class = EventPropositionForm
    template_name = 'events/propose.html'

    def get_form(self):
        return EventPropositionForm(self.request.user)

    def form_valid(self, form):
        if self.request.user.profile.is_member():
            subject = "[JDRPoly] Proposition d'event %s" % form.cleaned_data['name']
            to = (settings.EVENT_PROPOSITION_EMAIL, )
            content = form.cleaned_data['description']
            send_mail(subject, content, self.request.user.email, to)
            return super(EventPropositionView, self).form_valid(form)


class RegisterEditionView(UpdateView, LoginRequiredMixin):
    model = Edition

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.participants.add(request.user)
        obj.save()
        return redirect_to_edition(obj.pk)


class UnregisterEditionView(UpdateView, LoginRequiredMixin):
    model = Edition

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.participants.remove(request.user)
        obj.save()
        return redirect_to_edition(obj.pk)


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
        context = super(EventDetailView, self).get_context_data(*args,
                                                                **kwargs)
        context['editions'] = kwargs['object'].editions.all()
        context['editions'] = context['editions'].filter(date__gt=timezone.now())
        context['editions'] = context['editions'].order_by('-date')[:5].reverse()
        return context


class AttendingView(ListView, LoginRequiredMixin):
    template_name = 'events/attending.html'
    context_object_name = 'events'

    def get_queryset(self):
        return self.request.user.events.filter(date__gt=timezone.now())


class EditionDetailView(DetailView):
    model = Edition
    template_name = 'events/edition_view.html'
    context_object_name = 'edition'

    def get_context_data(self, *args, **kwargs):
        context = super(EditionDetailView, self).get_context_data(*args,
                                                                  **kwargs)
        obj = self.get_object()
        context['attending'] = self.request.user in obj.participants.all()
        return context


class RegisterParticipationView(UpdateView, LoginRequiredMixin):
    model = Event
    template_name = 'events/register.html'
