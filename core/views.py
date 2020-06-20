from dal import autocomplete
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from photologue.models import Photo

from core.forms import PhotoForm, GalleryForm, User
from core.models import ImanagerGallery


def homepage(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("accounts:login")
    owned_galleries = ImanagerGallery.objects.filter(created_by_id=user.id).order_by("date_added")
    shared_galleries = ImanagerGallery.objects.filter(shared_with=user).order_by("date_added")
    context = {
        "owned": owned_galleries,
        "shared": shared_galleries
    }
    return render(request=request,
                  template_name="homepage.html",
                  context=context)


class GalleryViewSet(DetailView):
    model = ImanagerGallery
    pk_url_kwarg = "gallery_id"
    template_name = "gallery_detail.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, f"Login needed to access that information!")
            return redirect("accounts:login")
        self.object = self.get_object()
        if self.object.created_by == user or self.object.shared_with.filter(id=user.id).exists():
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            messages.warning(request, f"Access Denied")
            return redirect("core:homepage")


class GalleryDeleteViewSet(DeleteView):
    model = ImanagerGallery
    pk_url_kwarg = "gallery_id"
    template_name = "gallery_delete.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, f"Login needed to access that information!")
            return redirect("accounts:login")
        return super(GalleryDeleteViewSet, self).get(request)

    def get_success_url(self):
        messages.success(self.request, f"Gallery deleted successfully!")
        return f"{settings.PROJECT_URL}{redirect('core:homepage').url}"


class GalleryCreationViewSet(CreateView):
    model = ImanagerGallery
    form_class = GalleryForm
    template_name = "gallery_creation.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, f"Login needed to access that information!")
            return redirect("accounts:login")
        return super(GalleryCreationViewSet, self).get(request)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if self.request.user and self.request.user.is_authenticated:
            self.object = form.save(user=self.request.user)
        messages.success(self.request, f"Gallery added successfully!")
        return HttpResponseRedirect(self.get_success_url())


class GalleryEditViewSet(UpdateView):
    model = ImanagerGallery
    form_class = GalleryForm
    template_name = "gallery_edit.html"
    pk_url_kwarg = "gallery_id"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, f"Login needed to access that information!")
            return redirect("accounts:login")
        return super(GalleryEditViewSet, self).get(request)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if self.request.user and self.request.user.is_authenticated:
            self.object = form.save(user=self.request.user)

        messages.success(self.request, f"Gallery edited successfully!")
        return HttpResponseRedirect(self.get_success_url())


class PhotoCreationViewSet(CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "image_creation.html"
    success_url = "core:gallery"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, f"Login needed to access that information!")
            return redirect("accounts:login")
        return super(PhotoCreationViewSet, self).get(request)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if self.kwargs["gallery_id"] and self.request.user.is_authenticated:
            self.object = form.save(gallery_id=self.kwargs["gallery_id"])
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        """Return the URL to redirect to after processing a valid form."""
        gallery_id = self.kwargs["gallery_id"]
        messages.success(self.request, f"Photo added successfully!")
        return f"{settings.PROJECT_URL}{redirect('core:gallery', int(gallery_id)).url}"


class PhotoEditViewSet(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "image_creation.html"
    pk_url_kwarg = "photo_id"
    success_url = "core:gallery"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, f"Login needed to access that information!")
            return redirect("accounts:login")
        return super(PhotoEditViewSet, self).get(request)

    def get_success_url(self, *args, **kwargs):
        """Return the URL to redirect to after processing a valid form."""
        gallery_id = self.kwargs["gallery_id"]
        messages.success(self.request, f"Photo edited successfully!")
        return f"{settings.PROJECT_URL}{redirect('core:gallery', int(gallery_id)).url}"


class PhotoDeleteViewSet(DeleteView):
    model = Photo
    pk_url_kwarg = "photo_id"
    template_name = "image_delete.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.warning(request, f"Login needed to access that information!")
            return redirect("accounts:login")
        return super(PhotoDeleteViewSet, self).get(request)

    def get_success_url(self):
        gallery_id = self.kwargs["gallery_id"]
        messages.success(self.request, f"Photo deleted successfully!")
        return f"{settings.PROJECT_URL}{redirect('core:gallery', gallery_id).url}"

