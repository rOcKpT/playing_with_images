from django.contrib import admin
from photologue.admin import GalleryAdmin

from core.models import ImanagerGallery

@admin.register(ImanagerGallery)
class ImanagerGalleryAdmin(GalleryAdmin):
    # list_display = ("title", "created_by")
    filter_horizontal = ("shared_with",)
