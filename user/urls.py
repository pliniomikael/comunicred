from django.urls import path
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("relatorios/", views.relatorios, name="relatorios"),
    # path("colaboradores/", views.colaboradores, name="colaboradores"),
    # path("login/", views.loginpage, name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout")
]
