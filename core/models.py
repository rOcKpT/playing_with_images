from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from photologue.models import Gallery
from django.utils.translation import ugettext_lazy as _

from imanager import settings


class ImanagerGallery(Gallery):
    created_by = models.ForeignKey(to=User, verbose_name="Created by", null=True, blank=True, on_delete=models.CASCADE, related_name="creator")
    shared_with = models.ManyToManyField(to=User, verbose_name="Shared Users", null=True, blank=True)

    class Meta:
        db_table = 'core_gallery'
        verbose_name = _("Imanager Gallery")
        verbose_name_plural = _("Imanager Galleries")

    class Menu:
        icon = "fa-th-list"

    @property
    def get_photos(self):
        return self.photos.all()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"{settings.PROJECT_URL}/gallery/{self.id}/"


    def save(self, *args, **kwargs):

        # if not self.id:
        #     self.created_by = 1
        if not self.slug:
            self.slug = slugify(self.title)
        return super(ImanagerGallery, self).save(*args, **kwargs)
