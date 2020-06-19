from django.shortcuts import render

from core.models import ImanagerGallery


def homepage(request):
    user = request.user
    owned_galleries = ImanagerGallery.objects.filter(created_by_id=user.id).order_by("date_added")
    shared_galleries = ImanagerGallery.objects.filter(shared_with=user).order_by("date_added")
    context = {
        "owned": owned_galleries,
        "shared": shared_galleries
    }
    return render(request=request,
           template_name="homepage.html",
                  context=context)


class GalleryViewSet():
    pass