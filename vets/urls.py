from django.urls import path
from . import views

app_name = "vets"

urlpatterns = [
    path("clinics/", views.clinic_list, name="clinic_list"),
]
