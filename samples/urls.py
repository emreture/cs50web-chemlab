from django.urls import path
from . import views

app_name = "samples"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:sample_id>", views.sample_details, name="sample_details"),
    path("add/", views.add_sample, name="add_sample"),
]
