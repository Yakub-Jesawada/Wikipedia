from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("Newpage", views.Newpage, name="Newpage"),
    path("search", views.search, name="search"),
    path("random", views.rand, name="rand"),
]
