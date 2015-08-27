from django.conf.urls import url
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
                                        MonthArchiveView)

from .models import Picture
from .views import (GalleryListView, GalleryDetailView, PicturesListView,
                    PictureDetailView, PictureUploadView)

urlpatterns = [
    url(r'^$', GalleryListView.as_view(), name='gallery-list'),
    url(r'^gallery/(?P<pk>\d+)$', GalleryDetailView.as_view(),
        name='gallery-detail'),
    url(r'^pics$', PicturesListView.as_view(), name='pictures-list'),
    url(r'^pic/(?P<pk>\d+)$', PictureDetailView.as_view(),
        name='picture-detail'),
    url(r'^pic/new$', PictureUploadView.as_view(), name='picture-upload'),

    # Archive views for pictures
    url(r'^archive/$', ArchiveIndexView.as_view(model=Picture,
                                                date_field='date'),
        name='pictures-archive-index'),
    url(r'^archive/(?P<year>[0-9]{4})/',
        YearArchiveView.as_view(model=Picture, date_field='date'),
        name='pictures-archive-year'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/',
        MonthArchiveView.as_view(model=Picture, date_field='date',
                                 month_format='%m'))
]
