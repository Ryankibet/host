
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from myapp.credentials import LipanaMpesaPpassword, MpesaAccessToken
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
from requests.auth import HTTPBasicAuth



# Create your views here.

def index(request):
    return render(request, "index.html")
    
def about(request):
    return render(request, "about.html")

def service(request):
    return render(request, "service.html")


def testimonial(request):
    return render(request, "testimonial.html")

def blog(request):
    return render(request, "blog.html")


@login_required(login_url='accounts:login')
def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user

            form.save()
            messages.success(request, "Your message has been sent successfully!")
            
        else:
            print(form.errors)  # Debugging: Outputs validation errors
            messages.error(request, "There was an error submitting the form. Please try again.")
    else:
        form = AppointmentForm()

    return render(request, 'appointment.html', {'form': form})

def team(request):
    return render(request, "mine.html")


@login_required
def appointment(request):
    if request.method == 'POST':
        contact = Appointment(
            name = request.POST.get('name'),
            date = request.POST.get('date'),
            email = request.POST.get('email'),
            phone = request.POST.get('phone'),
            message = request.POST.get('message'),
        )
        contact.save()
        
        # Redirect to a page after saving
        return redirect('myapp:appointment')  # Adjust the redirect to your desired page
    else:
        return render(request, 'appointment.html')
    

@login_required
def retrieve_appointments(request):
    appointments = Appointment.objects.all()
    context = {'appointments':appointments}
    return render(request, 'show_appointments.html', context)
 

def delete_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect("myapp:show_appointments")

def update_appointment(request, appointment_id):
    appointment =get_object_or_404(Appointment, id=appointment_id )
    if request.method == 'POST':
        appointment.name = request.POST.get('name')
        appointment.date = request.POST.get('date')
        appointment.email = request.POST.get('email')
        appointment.message = request.POST.get('message')
        appointment.save()
        return redirect("myapp:show_appointments")
     
    context = {'appointment': appointment}
    return render(request, "update_appointment.html", context)

# Adding the mpesa functions

#Display the payment form
@login_required
def pay(request):
   """ Renders the form to pay """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'A0lFhp6Kw10Ugb8mrjnv2jI59wFNslVV3dra99YHn3BFUb75'
    consumer_secret = 'qKJfOMvZz6CiogCbYo2ofWFfMsIIekt9ebmPoqH7TO3y4fX0EUXg7o0X8v0F7FNq'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")
