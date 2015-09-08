from django.views.generic import ListView, DetailView, View

from random import randint
from .models import News
from events.models import Event


class MainPageView(ListView):
    """
    View responsible for fetching latest news and displaying them
    """

    model = News
    context_object_name = 'latest_news'
    template_name = 'mainpage.html'

    def get_queryset(self):
        return News.objects.order_by('-date')[:5]

    def get_context_data(self, *args, **kwargs):
        context = super(MainPageView, self).get_context_data(*args, **kwargs)
        pk = randint(1, Event.objects.all().count() - 1)
        rng = (pk, pk + 1)
        context['notes'] = Event.objects.filter(pk__in=rng)
        return context


class NewsDetailView(DetailView):
    """
    View pour voir un article de news entier
    """

    model = News
    context_object_name = 'news'
    template_name = 'news/view.html'


class ContactFormHandleView(View):
    """
    View pour traiter le contenu du formulaire de contact
    """
    pass
