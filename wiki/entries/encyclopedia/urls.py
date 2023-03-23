from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hello/", views.hello, name="hello"),
    path("<str:article>", views.article, name="article"),
    path("search/", views.search, name="search"),
    path("new/", views.new_page, name="new"),
    path("edit/", views.edit, name="edit"),
    path("edit-save/", views.edit_save, name="edit-save"),
    path("random/", views.random, name="random")
]
