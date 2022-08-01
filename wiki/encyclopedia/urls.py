from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/", views.random_page, name="random"),
    path("search", views.search, name="search"),
]
