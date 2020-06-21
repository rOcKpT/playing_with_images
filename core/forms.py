from django.contrib.admin.widgets import *
from photologue.models import Photo

from .models import *


class GalleryForm(forms.ModelForm):

    class Meta:
        model = ImanagerGallery
        fields = ['title', 'description', 'created_by', 'shared_with']
        exclude = ["created_by"]
        labels = {
            'shared_with': ('Share with'),
        }
        widgets = {
            'shared_with': forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True, user=None):
        """
        Save this form's self.instance object if commit=True. Otherwise, add
        a save_m2m() method to the form which can be called after the instance
        is saved manually at a later time. Return the model instance.
        """
        if self.instance.created_by != user and not self.instance.id:
            self.instance.created_by = user
        return super(GalleryForm, self).save(commit)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']

    def save(self, commit=True, gallery_id=None):
        """
        Save this form's self.instance object if commit=True. Otherwise, add
        a save_m2m() method to the form which can be called after the instance
        is saved manually at a later time. Return the model instance.
        """
        add_gallery = False
        if gallery_id and not self.instance.id:
            add_gallery = True
        if not self.instance.slug:
            self.instance.slug = slugify(self.instance.title)

        super(PhotoForm, self).save(commit)

        if add_gallery:
            self.instance.galleries.add(gallery_id)
        return self.instance