from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.visit_entry, name="wiki"),
    path("searching", views.searching, name="searching"),
    path("search/<str:query>", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit/<str:entry>", views.edit, name="edit")
]
