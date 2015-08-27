from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from members.views import LoginRequiredMixin
from .models import Gallery, Picture


class GalleryListView(ListView):
    model = Gallery
    template_name = 'gallery/list.html'
    context_object_name = 'gallery_list'

    def get_queryset(self):
        return Gallery.objects.order_by('-date')[:10]


class GalleryDetailView(DetailView):
    model = Gallery
    template_name = 'gallery/view.html'
    context_object_name = 'gallery'


class PicturesListView(ListView):
    model = Picture
    template_name = 'pictures/list.html'
    context_object_name = 'picture_list'

    def get_queryset(self):
        return Picture.objects.order_by('-date')[:10]


class PictureDetailView(DetailView):
    model = Picture
    template_name = 'pictures/view.html'
    context_object_name = 'picture'


class PictureUploadView(CreateView, LoginRequiredMixin):
    model = Picture
    template_name = 'pictures/upload.html'
    success_url = reverse_lazy('pictures-list')


class GalleryCreateView(CreateView, LoginRequiredMixin):
    model = Gallery
    template_name = 'gallery/create.html'
    success_url = reverse_lazy('gallery-list')


class PictureDeleteView(DeleteView, LoginRequiredMixin):
    model = Picture
    template_name = 'gallery/delete.html'
    success_url = reverse_lazy('pictures-list')
