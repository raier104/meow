from django.shortcuts import render
from .models import VetClinic

def index(request):
    return render(request, "vets/index.html")

def clinic_list(request):
    clinics = VetClinic.objects.all()
    return render(request, "vets/clinic_list.html", {"clinics": clinics})
