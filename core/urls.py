from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("gallery/add/", views.GalleryCreationViewSet.as_view(), name="gallery_creation"),
    path("gallery/<int:gallery_id>/", views.GalleryViewSet.as_view(), name="gallery"),
    path("gallery/<int:gallery_id>/edit/", views.GalleryEditViewSet.as_view(), name="gallery_edit"),
    path("gallery/<int:gallery_id>/delete/", views.GalleryDeleteViewSet.as_view(), name="gallery_delete"),
    path("gallery/<int:gallery_id>/photo/add/", views.PhotoCreationViewSet.as_view(), name="photo_creation"),
    path("gallery/<int:gallery_id>/photo/<int:photo_id>/", views.PhotoCreationViewSet.as_view(), name="photo"),
    path("gallery/<int:gallery_id>/photo/<int:photo_id>/edit/", views.PhotoEditViewSet.as_view(), name="photo_edit"),
    path("gallery/<int:gallery_id>/photo/<int:photo_id>/delete/", views.PhotoDeleteViewSet.as_view(),
         name="photo_delete"),


]
