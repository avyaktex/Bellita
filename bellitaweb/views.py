from django.contrib.auth.decorators import login_required
from .models import Form, Services_by_cat
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
# from django.template.loader import render_to_string
# from premailer import Premailer
# from django.core.mail import EmailMessage
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib

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


# def send_email_user(subject, html_body, sender, recipients, smtp_server, smtp_port, username, password):
#     # Create a multipart message
#     message = MIMEMultipart()
#     message["Subject"] = subject
#     message["From"] = sender
#     message["To"] = ', '.join(recipients)

#     # Add the body of the email as HTML
#     message.attach(MIMEText(html_body, "html"))

#     # Connect to the SMTP server
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(username, password)

#         # Send the email
#         server.send_message(message)


# def send_email_admin(subject, html_body, sender, recipients, smtp_server, smtp_port, username, password):
#     # Create a multipart message
#     message = MIMEMultipart()
#     message["Subject"] = subject
#     message["From"] = sender
#     message["To"] = ', '.join(recipients)

#     # Add the body of the email as HTML
#     message.attach(MIMEText(html_body, "html"))

#     # Connect to the SMTP server
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(username, password)

#         # Send the email
#         server.send_message(message)


def appointment(request):
    services = Services_by_cat.objects.all().order_by('id')
    context = {
        'services' : services,
    }
    if request.method == 'POST':
        input_name = request.POST.get('input_name')
        mobile_number = request.POST.get('mobile_number')
        date = request.POST.get('date')
        email = request.POST.get('email')
        selected_services = ', '.join(request.POST.getlist('selectedServices'))
        form_data = Form(input_name=input_name, mobile_number=mobile_number, date=date, email=email, selected_services=selected_services)
        form_data.save()
        appointments = Form.objects.latest('id')
        # subject = "You have received a new appointment..."
        # sender = "avyaktex@gmail.com"
        # recipient_user = [email]
        # recipient_admin = ['parasm12345@gmail.com','dhrumilsheth1512@gmail.com']
        # smtp_server = "smtp.gmail.com"
        # smtp_port = 587
        # username = "avyaktex@gmail.com"
        # password = "lcxkeugwmogaactc"

        # Render the HTML template with the provided context data
        # html_content_user = render_to_string('mail_temp_user.html', {'appointment': form_data})
        # html_content_admin = render_to_string('mail_temp_admin.html', {'appointment': form_data})

        # # Send the email
        # send_email_user(subject, html_content_user, sender, recipient_user, smtp_server, smtp_port, username, password)
        # send_email_admin(subject, html_content_admin, sender, recipient_admin, smtp_server, smtp_port, username, password)

        context = {
            'appointment': form_data,
            'appointment' : appointments,
        }
        return render(request, 'success.html', context)
    return render(request, 'appointment.html', context)
    
def dashboard(request):
    search_name = request.GET.get('input_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    delete_record = request.GET.get('delete')

    appointments = Form.objects.all().order_by('-id')
    
    if delete_record:
        appointments = Form.objects.filter(
            id__icontains=delete_record
        ).order_by('-id')
        appointments.delete()
        # if search_name and (start_date or end_date):
        #     appointments = Form.objects.filter(
        #         Q(input_name__icontains=search_name),
        #         Q(date__range=[start_date, end_date])
        #     ).order_by('-id')
        #     appointments.delete()  # Delete the filtered records
        # else:
        #     Form.objects.all().delete()  # Delete all records

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