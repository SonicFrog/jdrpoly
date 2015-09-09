from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, FormView, TemplateView

from django.forms import (Form, CharField, EmailField, Textarea, TextInput,
                          BooleanField)

from random import randint
from .models import News, MainPageSection
from members.views import LoginRequiredMixin
from members.models import user_is_staff
from events.models import Event


class MainPageView(ListView):
    """
    View responsible for fetching latest news and displaying them
    """

    model = News
    context_object_name = 'sections'
    template_name = 'mainpage.html'

    def get_queryset(self):
        return MainPageSection.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(MainPageView, self).get_context_data(*args, **kwargs)
        pk = randint(1, Event.objects.all().count() - 1)
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


class NewsletterForm(Form):
    subject = CharField(widget=TextInput(attrs={'placeholder': _("Sujet")}))
    content = CharField(widget=Textarea(attrs={'placeholder': _("Contenu")}))
    member_only = BooleanField()

    def send_mail(self):
        to = []
        member_only = self.cleaned_data['member_only']

        userset = (User.objects.filter(profile__until__gt=timezone.now())
                   if member_only
                   else User.objects.all())

        userset = userset.filter(profile__wants_newsletter=True)

        to = [user.email for user in userset]
        subject = self.cleaned_data['subject']
        content = self.cleaned_data['content']
        send_mail(subject, content, settings.CONTACT_EMAIL, to)


class NewsletterSendView(FormView, LoginRequiredMixin):
    form_class = NewsletterForm
    template_name = 'news/letter.html'

    @method_decorator(user_passes_test(user_is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(NewsletterSendView, self).dispatch(request, *args,
                                                        **kwargs)

    def form_valid(self, form):
        form.send_mail()
        return super(NewsletterSendView, self).form_valid(form)


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
