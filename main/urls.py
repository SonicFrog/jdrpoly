from django.conf.urls import url
from .views import MainPageView, NewsDetailView, ContactFormHandleView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainpage'),
    url(r'^(?P<pk>\d+)$', NewsDetailView.as_view(), name='news-detail'),
    url(r'^contact$', ContactFormHandleView.as_view(), name='contact-handle'),
]
