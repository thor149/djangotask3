from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .google_calendar import create_calendar_event
from django.utils import timezone
from datetime import datetime, timedelta
import logging

//update
@login_required
def list_doctors(request):
    doctors = Profile.objects.filter(account_user_type='doctor')
    return render(request, 'appointmentScheduler/list_doctors.html', {'doctors': doctors})

@login_required
def book_appointment(request, pk):
    if request.user.profile.account_user_type != 'patient':
        raise PermissionDenied("Only patients can book appointments.")

    doctor = Profile.objects.get(id=pk)
    if doctor.account_user_type != 'doctor':
        raise PermissionDenied("You can only book appointments with doctors.")

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user.profile
            appointment.save()
            try:
                # Ensure valid emails
                if not appointment.doctor.user.email or not appointment.patient.user.email:
                    raise ValueError("Both doctor and patient must have valid email addresses.")

                # Create Google Calendar Event
                create_calendar_event(appointment)
                messages.success(request, 'Appointment booked successfully')
                return redirect('appointment_details', pk=appointment.id)
            except Exception as e:
                messages.error(request, f'Failed to create calendar event: {e}')
    else:
        form = AppointmentForm()
    return render(request, 'appointmentScheduler/book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def appointment_details(request, pk):
    appointment = Appointment.objects.get(id=pk)
    # Convert times to local timezone
    start_datetime = datetime.combine(appointment.appointment_date, appointment.start_time)
    end_datetime = datetime.combine(appointment.appointment_date, appointment.end_time)
    
    if timezone.is_naive(start_datetime):
        start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
    if timezone.is_naive(end_datetime):
        end_datetime = timezone.make_aware(end_datetime, timezone.get_current_timezone())
    
    start_time_local = timezone.localtime(start_datetime)
    end_time_local = timezone.localtime(end_datetime)
    
    context = {
        'appointment': appointment,
        'start_time_local': start_time_local,
        'end_time_local': end_time_local,
    }
    return render(request, 'appointmentScheduler/appointment_details.html', context)

def oauth2callback(request):
    return redirect('list_doctors')
