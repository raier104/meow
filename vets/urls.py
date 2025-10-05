from django.urls import path
from . import views

app_name = "vets"

urlpatterns = [
    path("clinics/", views.clinic_list, name="clinic_list"),
    path("vet-list/", views.clinic_doctor_list, name="clinic_doctor_list"),
    path("book/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("appointment/<int:appointment_id>/", views.appointment_detail, name="appointment_detail"),
    path("download-appointments/", views.download_appointments, name="download_appointments"),
    path("download-appointment/<int:appointment_id>/", views.download_appointment, name="download_appointment"),
]
