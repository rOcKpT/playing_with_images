from django.urls import path

from accounts import views


app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
]
