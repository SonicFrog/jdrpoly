# coding: utf-8

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail, send_mail
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, FormView, TemplateView

from django.forms import (Form, CharField, EmailField, Textarea, TextInput,
                          NullBooleanField)

from random import randint
from .models import News, MainPageSection, ComityMember
from members.views import LoginRequiredMixin
from events.models import Event

from members.models import user_is_staff


class MainPageView(ListView):
    """
    View responsible for fetching latest news and displaying them
    """
    context_object_name = 'sections'
    template_name = 'mainpage.html'

    def get_queryset(self):
        return MainPageSection.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(MainPageView, self).get_context_data(*args, **kwargs)
        evt_count = Event.objects.all().count() - 1
        if evt_count is not -1:
            pk = randint(0, evt_count)
            rng = (pk, pk + 1)
            context['notes'] = Event.objects.filter(pk__in=rng)
        context['latest_news'] = News.objects.order_by('-date')[:5]
        return context


class NewsDetailView(DetailView):
    """
    View pour voir un article de news entier
    """

    model = News
    context_object_name = 'news'
    template_name = 'news/view.html'


class ContactForm(Form):
    name = CharField(widget=TextInput(attrs={'placeholder': _("Nom")}))
    email = EmailField(widget=TextInput(attrs={'placeholder': _("Email")}))
    message = CharField(widget=Textarea(attrs={'placeholder': _("Message")}))

    def send_mail(self):
        to = (settings.CONTACT_EMAIL, )
        subject = "Formulaire de contact JDRpoly"
        content = self.cleaned_data['message']
        sender = "%s <%s>" % (self.cleaned_data['name'],
                              self.cleaned_data['email'])
        send_mail(subject, content, sender, to)
        return to


class NewsletterForm(Form):
    subject = CharField(widget=TextInput(attrs={'placeholder': _("Sujet")}))
    content = CharField(widget=Textarea(attrs={'placeholder': _("Contenu")}))
    member_only = BooleanField()

    def send_mail(self):
        member_only = self.cleaned_data['member_only']

        userset = (User.objects.filter(profile__until__gt=timezone.now())
                   if member_only
                   else User.objects.all())

        userset = userset.filter(profile__wants_newsletter__exact=True)

        bcc = [user.email for user in userset]
        subject = self.cleaned_data['subject']
        content = self.cleaned_data['content']
        messages = []
        for mail in bcc:
            message = (subject, content, settings.DEFAULT_FROM_EMAIL, [mail])
            messages.append(message)
        send_mass_mail(messages)


class NewsletterSendView(LoginRequiredMixin, FormView):
    form_class = NewsletterForm
    template_name = 'news/letter.html'
    success_url = reverse_lazy('newsletter-success')

    @method_decorator(user_passes_test(user_is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(NewsletterSendView, self).dispatch(request, *args,
                                                        **kwargs)

    def form_valid(self, form):
        form.send_mail()
        return super(NewsletterSendView, self).form_valid(form)


class NewsletterSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'news/letter_ok.html'


class ContactFormHandleView(FormView):
    """
    View pour traiter le contenu du formulaire de contact
    """
    form_class = ContactForm
    success_url = reverse_lazy('contact-success')
    template_name = 'contact.html'

    def form_valid(self, form):
        form.send_mail()
        return super(ContactFormHandleView, self).form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'contact_success.html'


class ComityListView(ListView):
    """
    Vue pour les membres actuels du comité
    """
    model = ComityMember
    template_name = 'comity.html'
    context_object_name = 'comity'
