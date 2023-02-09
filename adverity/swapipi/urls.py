from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dataset/<uuid:uid>", views.dataset, name="dataset"),
    path("value_count/<uuid:uid>", views.value_count, name="value_count"),
    path("api/collect_entries/", views.collect_entries, name="collect_entries"),
]
