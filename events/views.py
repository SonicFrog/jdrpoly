# coding: utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
import django.contrib.messages as messages
from django.shortcuts import HttpResponseRedirect, Http404
from django.views.generic import (DetailView, ListView, FormView,
                                  CreateView, DeleteView, UpdateView)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import datetime

from .forms import EventPropositionForm, CampaignCreateForm
from .models import Event, Edition, Campaign
from members.views import LoginRequiredMixin, MembershipRequiredMixin


def redirect_to_edition(pk):
    return HttpResponseRedirect(reverse_lazy('edition-detail',
                                             kwargs={'pk': pk}))


def redirect_to_campaign(pk):
    return HttpResponseRedirect(reverse_lazy('campaign-detail',
                                             kwargs={'pk': pk}))


class CampaignToggleEnrollView(LoginRequiredMixin, UpdateView):
    model = Campaign

    def get(self, request, *args, **kwargs):
        camp = self.get_object()
        if request.user.profile.is_enrolled_in(camp):
            camp.unregister_user(request.user)
            messages.success(self.request, _("Inscrit avec succès !"))
        else:
            messages.success(self.request, _("Désinscrit avec succès !"))
            camp.register_user(request.user)
        return redirect_to_campaign(camp.pk)


class CampaignDeleteView(SuccessMessageMixin, MembershipRequiredMixin,
                         DeleteView):
    model = Campaign
    template_name = 'events/campaign_delete.djhtml'
    success_url = reverse_lazy('campaign-list')
    success_message = _("Campagne %(name)s supprimée avec succès !")

    def form_valid(self, form):
        if self.get_object().owner is self.request.user:
            return super(CampaignDeleteView, self).form_valid(form)
        else:
            return Http404()


class CampaignPropositionView(MembershipRequiredMixin, CreateView):
    model = Campaign
    template_name = 'events/new_campaign.djhtml'
    form_class = CampaignCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CampaignPropositionView, self).form_valid(form)


class MyCampaignView(MembershipRequiredMixin, ListView):
    model = Campaign
    template_name = 'events/campaign_list.djhtml'
    context_object_name = 'campaign_list'

    def get_context_data(self):
        context = super(MyCampaignView, self).get_context_data()
        context['title'] = _("Mes campagnes")
        return context

    def get_queryset(self):
        user = self.request.user
        all_runs = Campaign.objects.filter(running=True)
        participating = all_runs.filter(participants__in=[user.pk])
        organising = all_runs.filter(owner=user)
        return participating | organising


class CampaignUpdateView(SuccessMessageMixin, MembershipRequiredMixin,
                         UpdateView):
    model = Campaign
    template_name = 'events/campaign_edit.djhtml'
    success_message = _("Campagne modifiée avec succès !")

    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().owner:
            return super(CampaignUpdateView, self).post(request, *args, **kwargs)
        return Http404()

    def get_success_url(self):
        return reverse_lazy('campaign-detail', kwargs={'pk': self._id})


class CampaignDetailView(MembershipRequiredMixin, DetailView):
    model = Campaign
    template_name = 'events/campaign_detail.djhtml'
    context_object_name = 'campaign'


class CampaignListView(MembershipRequiredMixin, ListView):
    model = Campaign
    template_name = 'events/campaign_list.djhtml'
    context_object_name = 'campaign_list'

    def get_queryset(self):
        cset = Campaign.objects.filter(running=True)
        return cset.filter(open_for_registration=True).order_by('-start')


class EventPropositionView(FormView, LoginRequiredMixin):
    form_class = EventPropositionForm
    template_name = 'events/propose.djhtml'

    def get_form(self):
        return EventPropositionForm(self.request.user)

    def form_valid(self, form):
        if self.request.user.profile.is_member():
            subject = "[JDRPoly] Proposition d'event %s" % form.cleaned_data['name']
            to = (settings.EVENT_PROPOSITION_EMAIL, )
            content = form.cleaned_data['description']
            send_mail(subject, content, self.request.user.email, to)
            return super(EventPropositionView, self).form_valid(form)


class RegisterEditionView(LoginRequiredMixin, UpdateView):
    model = Edition

    def get(self, request, *args, **kwargs):
        self.get_object().register_user(request.user)
        return redirect_to_edition(self.get_object().pk)


class UnregisterEditionView(LoginRequiredMixin, UpdateView):
    model = Edition

    def get(self, request, *args, **kwargs):
        self.get_object().unregister_user(request.user)
        return redirect_to_edition(self.get_object().pk)


class EventListView(ListView):
    template_name = 'events/list.djhtml'
    name = 'event-list'
    context_object_name = 'event_list'
    model = Event


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/view.djhtml'
    context_object_name = 'event'

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetailView, self).get_context_data(*args,
                                                                **kwargs)
        context['editions'] = kwargs['object'].editions.all()
        valid_date = timezone.now() - datetime.timedelta(1)
        context['editions'] = context['editions'].filter(date__gt=valid_date)
        context['editions'] = context['editions'].order_by('-date')[:5].reverse()
        return context


class AttendingView(LoginRequiredMixin, ListView):
    template_name = 'events/attending.djhtml'
    context_object_name = 'events'

    def get_queryset(self):
        return self.request.user.events.filter(date__gt=timezone.now())


class EditionDetailView(DetailView):
    model = Edition
    template_name = 'events/edition_view.djhtml'
    context_object_name = 'edition'

    def get_context_data(self, *args, **kwargs):
        context = super(EditionDetailView, self).get_context_data(*args,
                                                                  **kwargs)
        obj = self.get_object()
        context['attending'] = self.request.user in obj.participants.all()
        return context


class RegisterParticipationView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/register.djhtml'


class HtmlEventList(ListView):
    """
    View for dynamic event menu generation
    """
    model = Event
    template_name = 'events/menu_event.djhtml'
    context_object_name = 'event_list'
