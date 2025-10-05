from django.shortcuts import render
from .models import VetClinic, Doctor, TimeSlot
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
def clinic_doctor_list(request):
    clinics = VetClinic.objects.all()
    return render(request, "vets/clinic_doctor_list.html", {"clinics": clinics})

def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    timeslots = TimeSlot.objects.filter(doctor=doctor, is_available=True)
    if request.method == "POST":
        # Here you would create an Appointment object, mark slot as booked, etc.
        slot_id = request.POST.get("time")
        slot = get_object_or_404(TimeSlot, id=slot_id, doctor=doctor, is_available=True)
        slot.is_available = False
        slot.save()
        messages.success(request, "Appointment booked!")
        return redirect("vets:clinic_doctor_list")
    return render(request, "vets/book_appointment.html", {"doctor": doctor, "timeslots": timeslots})

def index(request):
    return render(request, "vets/index.html")

def clinic_list(request):
    clinics = VetClinic.objects.all()
    from daycare.models import Daycare
    daycares = Daycare.objects.all()
    return render(request, "daycare/clinic_list.html", {"clinics": clinics, "daycares": daycares})
