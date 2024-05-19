from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.page, name="page"),
    path("results/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("save", views.save_after_edit, name="save"),
    path("random", views.random_page, name="random_page")
]
