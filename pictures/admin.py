from django.contrib import admin
from .models import Picture, Gallery


class PictureAdmin(admin.ModelAdmin):
    list_display = ('comment', 'owner', 'date')


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Picture, PictureAdmin)
