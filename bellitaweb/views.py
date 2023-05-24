from django.contrib.auth.decorators import login_required
from .models import Form
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
@login_required
def restricted_view(request):
    return render(request, 'dashboard.html')

def index(request):
    return render(request, 'index.html')

def success(request):
    appointments = Form.objects.latest()
    context = {
        'appointment' : appointments,
    }
    return render(request, 'success.html', context)

def appointment(request):
    if request.method == 'POST':
        input_name = request.POST.get('input_name')
        mobile_number = request.POST.get('mobile_number')
        date = request.POST.get('date')
        email = request.POST.get('email')
        form_data = Form(input_name=input_name, mobile_number=mobile_number, date=date, email=email)
        form_data.save()
        appointments = Form.objects.latest('id')
        context = {
            'appointment' : appointments,
        }
        return render(request, 'success.html', context)
    else:
        return render(request, 'appointment.html')


def dashboard(request):
    search_name = request.GET.get('input_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    delete_record = request.GET.get('delete')

    appointments = Form.objects.all().order_by('-id')
    
    if delete_record:
        if search_name and (start_date or end_date):
            appointments = Form.objects.filter(
                Q(input_name__icontains=search_name),
                Q(date__range=[start_date, end_date])
            ).order_by('-id')
            appointments.delete()  # Delete the filtered records
        else:
            Form.objects.all().delete()  # Delete all records

    if search_name and (start_date or end_date):
        appointments = Form.objects.filter(
            Q(input_name__icontains=search_name),
            Q(date__range=[start_date, end_date])
        ).order_by('-id')
    elif search_name:
        appointments = Form.objects.filter(input_name__icontains=search_name).order_by('-id')
    elif start_date and end_date:
        appointments = Form.objects.filter(date__range=[start_date, end_date]).order_by('-id')
    else:
        appointments = Form.objects.all().order_by('-id')
        

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