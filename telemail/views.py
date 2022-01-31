from django.shortcuts import render
from rest_framework import serializers, viewsets
from .models import *
from PIL.Image import new
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, FormView, TemplateView, DetailView, ListView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AdminPasswordChangeForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
import sendgrid
from sendgrid.helpers.mail import *
from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from decouple import config, Csv
import datetime
import base64
import json 
import random
import base64
from io import BytesIO
from .forms import * 
import json
from .tasks import * 
import asyncio 

# Create your views here.
#Homepage Landing Page
def Homepage(request):
    
    if request.method == "POST":

        form = telegram_userForm(request.POST)
        if form.is_valid():
            prev = form.save(commit=False)
            user_email = prev.email
            prev.save()

            end_date = datetime.now()
            start_date = end_date - timedelta(days=1)

            allMessages = pinnedMessage.objects.filter(timestamp__range=[start_date, end_date], is_sent=False).order_by('timestamp')
            message = Mail(
                from_email='audrey@nanupanda.com',
                to_emails=user_email ,
                subject='CPG Club',
                html_content=get_template('summary_email.html').render({'allMessages': allMessages[:10]}))
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                pass

        return redirect('confirmation')

    else:

        form = telegram_userForm()
    return render(request, "home.html", {'form': form})

def Confirmation(request):
    confirmation = True 
    return render(request, "home.html", {'confirmation': confirmation })


@csrf_exempt 
def AddMessage(request):
    if request.method == "POST":
        messages = json.loads(request.body)
        for mess in messages:
            new_pin, _ = pinnedMessage.objects.get_or_create(pmesssage=int(mess["id"]))
            new_pin.message = mess["message"]
            new_pin.save()
        # serialize in new friend object in json
        #mess_id = request.GET['id']
        #message = request.GET['message']
        #print(mess_id, message)
        context = {"message": "Success"}
        return JsonResponse(context)
    else:

        context = {"message": "Failure"}
        return JsonResponse(context)




