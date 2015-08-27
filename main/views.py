from django.views.generic import ListView, DetailView

from .models import News


class MainPageView(ListView):
    """
    View responsible for fetching latest news and displaying them
    """

    model = News
    context_object_name = 'latest_news'
    template_name = 'mainpage.html'

    def get_queryset(self):
        return News.objects.order_by('-date')[:5]


class NewsDetailView(DetailView):
    """
    View pour voir un article de news entier
    """

    model = News
    context_object_name = 'news'
    template_name = 'news.html'
