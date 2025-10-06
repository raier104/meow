from django.shortcuts import render
from .models import VetClinic, Doctor, TimeSlot, Appointment
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
import json

def clinic_doctor_list(request):
    clinics = VetClinic.objects.all()
    return render(request, "vets/clinic_doctor_list.html", {"clinics": clinics})

def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(VetClinic, id=clinic_id)
    doctors = clinic.doctor_set.all()
    return render(request, "vets/clinic_detail.html", {"clinic": clinic, "doctors": doctors})

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    timeslots = TimeSlot.objects.filter(doctor=doctor, is_available=True).order_by('start')
    
    if request.method == "POST":
        slot_id = request.POST.get("time")
        
        # Check if slot_id exists and is valid
        if not slot_id:
            messages.error(request, "Please select a time slot.")
            return render(request, "vets/book_appointment.html", {"doctor": doctor, "timeslots": timeslots})
        
        try:
            slot = get_object_or_404(TimeSlot, id=slot_id, doctor=doctor, is_available=True)
            
            # Create appointment record
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                time_slot=slot
            )
            
            # Mark slot as unavailable
            slot.is_available = False
            slot.save()
            
            messages.success(request, "Appointment booked successfully!")
            return redirect("vets:appointment_detail", appointment_id=appointment.id)
            
        except Exception as e:
            messages.error(request, "The selected time slot is no longer available. Please choose another slot.")
            return render(request, "vets/book_appointment.html", {"doctor": doctor, "timeslots": timeslots})
    
    return render(request, "vets/book_appointment.html", {"doctor": doctor, "timeslots": timeslots})

def get_time_slots(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    selected_date = request.GET.get('date')
    
    if not selected_date:
        return JsonResponse({'timeslots': []})
    
    try:
        # Parse the date
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        
        # Get time slots for the selected date
        timeslots = TimeSlot.objects.filter(
            doctor=doctor,
            is_available=True,
            start__date=date_obj
        ).order_by('start')
        
        # Format the time slots for JSON response
        slots_data = []
        for slot in timeslots:
            slots_data.append({
                'id': slot.id,
                'start_time': slot.start.strftime('%H:%M'),
                'end_time': slot.end.strftime('%H:%M'),
                'start_datetime': slot.start.isoformat(),
                'end_datetime': slot.end.isoformat()
            })
        
        return JsonResponse({'timeslots': slots_data})
        
    except ValueError:
        return JsonResponse({'timeslots': [], 'error': 'Invalid date format'})
    except Exception as e:
        return JsonResponse({'timeslots': [], 'error': str(e)})

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-booked_at')
    return render(request, "vets/my_appointments.html", {"appointments": appointments})

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    return render(request, "vets/appointment_detail.html", {"appointment": appointment})

@login_required
def download_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-booked_at')
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph(f"Veterinary Appointments - {request.user.get_full_name() or request.user.username}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # User info
    user_info = f"<b>Patient:</b> {request.user.get_full_name() or request.user.username}<br/>"
    user_info += f"<b>Email:</b> {request.user.email}<br/>"
    from django.utils import timezone
    user_info += f"<b>Generated on:</b> {timezone.now().strftime('%B %d, %Y, %I:%M %p')}"
    story.append(Paragraph(user_info, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Appointments
    for appointment in appointments:
        apt_text = f"<b>Dr. {appointment.doctor.name}</b><br/>"
        apt_text += f"<b>Clinic:</b> {appointment.doctor.clinic.name}<br/>"
        apt_text += f"<b>Specialization:</b> {appointment.doctor.specialization}<br/>"
        apt_text += f"<b>Date & Time:</b> {appointment.time_slot.start.strftime('%B %d, %Y, %I:%M %p')} - {appointment.time_slot.end.strftime('%I:%M %p')}<br/>"
        apt_text += f"<b>Fee:</b> {appointment.doctor.fee} TK<br/>"
        apt_text += f"<b>Address:</b> {appointment.doctor.clinic.address}<br/>"
        if appointment.doctor.clinic.phone:
            apt_text += f"<b>Phone:</b> {appointment.doctor.clinic.phone}<br/>"
        apt_text += f"<b>Booked on:</b> {appointment.booked_at.strftime('%B %d, %Y, %I:%M %p')}"
        
        story.append(Paragraph(apt_text, styles['Normal']))
        story.append(Spacer(1, 20))
    
    if not appointments:
        story.append(Paragraph("No appointments found.", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="my_appointments_{request.user.username}.pdf"'
    return response

@login_required
def download_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph(f"Appointment Confirmation - {request.user.get_full_name() or request.user.username}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # User info
    user_info = f"<b>Patient:</b> {request.user.get_full_name() or request.user.username}<br/>"
    user_info += f"<b>Email:</b> {request.user.email}<br/>"
    from django.utils import timezone
    user_info += f"<b>Generated on:</b> {timezone.now().strftime('%B %d, %Y, %I:%M %p')}"
    story.append(Paragraph(user_info, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Appointment details
    apt_text = f"<b>Dr. {appointment.doctor.name}</b><br/>"
    apt_text += f"<b>Clinic:</b> {appointment.doctor.clinic.name}<br/>"
    apt_text += f"<b>Specialization:</b> {appointment.doctor.specialization}<br/>"
    apt_text += f"<b>Date & Time:</b> {appointment.time_slot.start.strftime('%B %d, %Y, %I:%M %p')} - {appointment.time_slot.end.strftime('%I:%M %p')}<br/>"
    apt_text += f"<b>Fee:</b> {appointment.doctor.fee} TK<br/>"
    apt_text += f"<b>Address:</b> {appointment.doctor.clinic.address}<br/>"
    if appointment.doctor.clinic.phone:
        apt_text += f"<b>Phone:</b> {appointment.doctor.clinic.phone}<br/>"
    apt_text += f"<b>Booked on:</b> {appointment.booked_at.strftime('%B %d, %Y, %I:%M %p')}"
    
    story.append(Paragraph(apt_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="appointment_{appointment.id}_{request.user.username}.pdf"'
    return response

def index(request):
    return render(request, "vets/index.html")

def clinic_list(request):
    clinics = VetClinic.objects.all()
    from daycare.models import Daycare
    daycares = Daycare.objects.all()
    return render(request, "daycare/clinic_list.html", {"clinics": clinics, "daycares": daycares})
