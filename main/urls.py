from django.conf.urls import url
from .views import MainPageView, NewsDetailView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainpage'),
    url(r'^(?P<pk>\d+)$', NewsDetailView.as_view(), name='news-detail'),
]
