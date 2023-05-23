import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def services(request):
    return render(request, 'services.html')

def success(request):
    appointments = Form.objects.latest()
    context = {
        'appointment' : appointments,
    }
    return render(request, 'success.html', context)


def send_email(subject, body, sender, recipients, smtp_server, smtp_port, username, password):
    # Create a multipart message
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ', '.join(recipients)

    # Add the body of the email as plain text
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)

        # Send the email
        server.send_message(message)

def appointment(request):
    if request.method == 'POST':
        input_name = request.POST.get('input_name')
        mobile_number = request.POST.get('mobile_number')
        date = request.POST.get('date')
        form_data = Form(input_name=input_name, mobile_number=mobile_number, date=date)
        form_data.save()
        subject = "You have recieved a new appointment..."
        body = "A new appointment has been booked by " + input_name + " on " + date + ". Mobile number of the client is " + mobile_number + "."
        sender = "avyaktex@gmail.com"
        recipients = ["dhrumilsheth1512@gmail.com", "parasm12345@gmail.com"]
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        username = "avyaktex@gmail.com"
        password = "tooxbsopcagtjfor"
        send_email(subject, body, sender, recipients, smtp_server, smtp_port, username, password)
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