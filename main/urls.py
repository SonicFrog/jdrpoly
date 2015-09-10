from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainpage'),
    url(r'^(?P<pk>\d+)$', NewsDetailView.as_view(), name='news-detail'),
    url(r'^contact$', ContactFormHandleView.as_view(), name='contact-handle'),
    url(r'^contact_success$', ContactSuccessView.as_view(),
        name='contact-success'),
    url(r'^newsletter/$', NewsletterSendView.as_view(),
        name='newsletter-send'),
    url(r'^newsletter/success$', NewsletterSuccessView.as_view(),
        name='newsletter-success'),
    url(r'^comity/$', ComityListView.as_view(), name='comity-list'),
]
