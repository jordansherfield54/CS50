from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("jordan", views.jordan, name="jordan"),
    path("<str:name>", views.greet, name="greet")
]