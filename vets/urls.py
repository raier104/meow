from django.urls import path
from . import views

app_name = "vets"

urlpatterns = [
    path("my-clinic/", views.my_clinic, name="my_clinic"),
    path("clinics/", views.clinic_list, name="clinic_list"),
    path("vet-list/", views.clinic_doctor_list, name="clinic_doctor_list"),
    path("clinic/<int:clinic_id>/", views.clinic_detail, name="clinic_detail"),
    path("book/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path("get-time-slots/<int:doctor_id>/", views.get_time_slots, name="get_time_slots"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("appointment/<int:appointment_id>/", views.appointment_detail, name="appointment_detail"),
    path("download-appointments/", views.download_appointments, name="download_appointments"),
    path("download-appointment/<int:appointment_id>/", views.download_appointment, name="download_appointment"),
]
