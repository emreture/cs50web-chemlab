from django.urls import path
from . import views

app_name = "results"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:sample_id>", views.results, name="results")
]
