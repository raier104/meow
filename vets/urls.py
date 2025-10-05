from django.urls import path
from . import views

app_name = "vets"

urlpatterns = [
    path("clinics/", views.clinic_list, name="clinic_list"),
    path("vet-list/", views.clinic_doctor_list, name="clinic_doctor_list"),
    path("book/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
]
