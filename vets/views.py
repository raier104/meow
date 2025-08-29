from django.shortcuts import render
from .models import VetClinic

def index(request):
    return render(request, 'vets/index.html')  # create index.html template in vets/templates/vets/

def clinic_list(request):
    return render(request, "vets/user_selection.html")  # Render the user_selection.html template
    return render(request, "vets/clinic_list.html", {"clinics": clinics})
