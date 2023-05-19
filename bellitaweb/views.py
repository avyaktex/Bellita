import pywhatkit
from django.contrib.auth.decorators import login_required
from .models import FormData
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
@login_required
def restricted_view(request):
    return render(request, 'dashboard.html')

def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def success(request):
    return render(request, 'success.html')

def appointment(request):
    if request.method == 'POST':
        input_name = request.POST.get('input_name')
        mobile_number = request.POST.get('mobile_number')
        date = request.POST.get('date')
        time = request.POST.get('time')
        form_data = FormData(input_name=input_name, mobile_number=mobile_number, time=time, date=date)
        form_data.save()
        phone_number = "+916353222659"  # Replace with the recipient's phone number
        message =  "You have recieved a new appointment. The customer data is given below : Customer Name :" + input_name + "& Customer Mobile Number :" + mobile_number + "& Customer Booked Date :" + date + "& Customer Booked Time :" + time + "." # Replace with your desired message content
        hour =  16  #Replace with the desired hour
        minute = 36  #Replace with the desired minute

        pywhatkit.sendwhatmsg(phone_number, message, hour, minute)

        return render(request, 'success.html')
    else:
        return render(request, 'appointment.html')


def dashboard(request):
    search_name = request.GET.get('input_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # delete_record = request.GET.get('delete')

    appointments = FormData.objects.all().order_by('-id')
    
    # if delete_record:
    #     appointments = FormData.objects.all().delete()

    if search_name and (start_date or end_date):
        appointments = appointments.filter(
            Q(input_name__icontains=search_name),
            Q(date__range=[start_date, end_date])
        ).order_by('-id')
    elif search_name:
        appointments = appointments.filter(input_name__icontains=search_name).order_by('-id')
    elif start_date and end_date:
        appointments = appointments.filter(date__range=[start_date, end_date]).order_by('-id')

    # Create a Paginator object with a desired number of entries per page
    paginator = Paginator(appointments, 10)
    
    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page number
    page_obj = paginator.get_page(page_number)

    context = {
        'appointments': page_obj,
        'page_obj': page_obj,
        'search_name': search_name,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'dashboard.html', context)