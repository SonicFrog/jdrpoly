# coding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect
from django.forms import Form, ModelForm, CharField, Textarea, TextInput
from django.views.generic import (DetailView, ListView, UpdateView, FormView,
                                  CreateView)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import Event, Edition, Campaign
from members.views import LoginRequiredMixin


def redirect_to_edition(pk):
    return HttpResponseRedirect(reverse_lazy('edition-detail',
                                             kwargs={'pk': pk}))


def redirect_to_campaign(pk):
    return HttpResponseRedirect(reverse_lazy('campaign-detail',
                                             kwargs={'pk': pk}))


class CampaignCreateForm(ModelForm):
    def is_valid(self):
        if not super(CampaignCreateForm, self).is_valid():
            return False
        out = True
        if not self.start > timezone.now():
            self._errors.append('Votre campagne ne peut pas démarrer dans le passé !')
            out = False

        if not self.max_players > 0:
            self._errors.append('Votre campagne ne peut pas avoir un nombre négatif de joueurs !')
            out = False
        return out

    class Meta:
        model = Campaign
        fields = ['name', 'description', 'max_players', 'start', ]


class CampaignPropositionView(CreateView, LoginRequiredMixin):
    model = Campaign
    template_name = 'events/new_campaign.html'
    form_class = CampaignCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CampaignPropositionView, self).form_valid(form)


class CampaignDetailView(DetailView, LoginRequiredMixin):
    model = Campaign
    template_name = 'events/campaign_detail.html'
    context_object_name = 'campaign'


class CampaignListView(ListView, LoginRequiredMixin):
    model = Campaign
    template_name = 'events/campaign_list.html'
    context_object_name = 'campaign_list'

    def get_queryset(self):
        return Campaign.objects.filter(running=True).filter(open_for_registration=True).order_by('-start')


class CampaignRegisterView(UpdateView, LoginRequiredMixin):
    model = Campaign
    template_name = 'events/register_campaign.html'

    def post(self, request, *args, **kwargs):
        self.get_object().register_user(request.user)
        return super(CampaignRegisterView, self).post(request, *args, **kwargs)

    def get_context_data(self):
        context = super(UpdateView, self).get_context_data()
        object = self.get_object()
        context['registered'] = self.request.user in object.participants.all()
        return context


class CampaignUnregisterView(UpdateView, LoginRequiredMixin):
    model = Campaign

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.unregister_user(request.user)
        return redirect_to_campaign(obj.pk)


class EventPropositionForm(Form):
    name = CharField(max_length=100, label=False,
                     widget=TextInput(attrs={'placeholder':
                                             _('Nom de l\'évenement')}))
    description = CharField(widget=Textarea(attrs={'placeholder':
                                                   _('Description')}),
                            label=False,)

    def __init__(self, user, *args, **kwargs):
        super(EventPropositionForm, self).__init__(*args, **kwargs)
        self.user = user

    def is_valid(self):
        if not super(EventPropositionForm, self).is_valid():
            return False
        if not self.user.profile.is_member():
            self._errors = ['Vous ne pouvez pas proposer de soirées membres sans être membre']
            return False
        return True


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
        self.get_object().register_user(request.user)
        return redirect_to_edition(self.get_object().pk)


class UnregisterEditionView(UpdateView, LoginRequiredMixin):
    model = Edition

    def get(self, request, *args, **kwargs):
        self.get_object().unregister_user(request.user)
        return redirect_to_edition(self.get_object().pk)


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
