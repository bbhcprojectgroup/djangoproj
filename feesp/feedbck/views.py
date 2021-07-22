

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from typing import cast
from django.contrib import messages
#from django.contrib.auth import login,authenticate,logout
from feedbck.models import FeedBack

# Create your views here.
def feedback(request):
     if request.method =='POST':
         firstname=request.POST['firstname']
         lastname=request.POST['lastname']
         phone=request.POST['MobileNo']
         email=request.POST['mailId']
         feedback=request.POST['feedback']
         data = FeedBack(firstname=firstname, lastname=lastname, phone=phone, email=email, feedback=feedback)
         data.save()
         messages.success(request, 'Thankyou for your feedback') 
          #return render(request, 'base.html')
     return render(request, 'feedback.html')