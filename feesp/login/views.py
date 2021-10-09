from django.shortcuts import render,redirect
from django.http import HttpResponse
from typing import cast
import random,string
from twilio.rest import Client
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from login.models import Account,setCllegeInfo
from django.utils import timezone
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm,AuthenticationForm
from django.contrib.auth.views import PasswordResetConfirmView,LoginView
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required
from examfee.models import site_settings
from feesp import settings
import json
from django.utils.dateparse import parse_date,parse_time
from datetime import timedelta,datetime
import dateutil.parser
from acdfee.models import set_concession
#from django.contrib.admin.forms import AdminAuthenticationForm



# Create your views here.
def home(request):
    site=site_settings.objects.get()
    conc=set_concession.objects.all()
    cllegeInfo=setCllegeInfo.objects.get()
    return render(request,'home.html',{'context':site,'conc1':conc[0].percentage_concession,'conc2':conc[1].percentage_concession,'conc3':conc[2].percentage_concession,'clg':cllegeInfo})

def handler404(request, *args, **argv):
    response = render(request,'404.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request,'500.html', {})
    response.status_code = 500
    return response

"""def feedback(request):
    return render(request,'feedback.html')
class CustomAuthenticationForm(AdminAuthenticationForm):
     def clean(self):
        username = self.cleaned_data.get('username')
        password = encrypt(self.cleaned_data.get('password'))
        print(password)

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'"""


def encrypt(pssword):
    s1 = pssword[:len(pssword)//2]
    s2 = pssword[len(pssword)//2:]
    r1=s1[len(s1)::-1]
    r2=s2[len(s2)::-1]
    return r1+r2
    

class customSetPasswordForm(SetPasswordForm):
    def save(self, commit=True):
        password = encrypt(self.cleaned_data["new_password1"])
        print(password)
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class customPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = customSetPasswordForm

@requires_csrf_token   
def register(request):

    if (request.method =='POST'):
         username=request.POST['username']
         email=request.POST['email']
         if(Account.objects.filter(username=username).exists()):
              messages.success(request, 'username already exists') 
         elif(Account.objects.filter(email=email).exists()):
             messages.success(request, 'email already exists') 
         else:
             phone=request.POST['phone']
             password1=encrypt(request.POST['password'])
             print(password1)
             """user = Account.objects.create_user(username=username, phone=phone, email=email, password=password1)
             user.save()
             #request.session['username'] = user.username
             messages.success(request, 'user name created')   
    return render(request,'base.html')"""
             otp=''.join(random.choice(string.digits) for x in range(4))
             try:
                mail='your otp is to visit '+otp+' Apply Procedures'
            
                send_mail('One Time Password', mail, 'feepayportal@gmail.com' ,[email], fail_silently=False)
             except gaierror:
                print('oops')
             
             
             client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

             message = client.messages.create(
                                        messaging_service_sid='MG7b8f86e6946c32ae3229d0859b794d89', 
                                        body=f'Hi, your feepay otp is {otp}. Please enter this otp within 1 minute',
                                        to="+91"+phone 
                                        #to="+916362037635"
                                    )
             print(message.sid)
             request.session['username']=username
             request.session['password1']=password1
             request.session['phone']=phone
             request.session['email']=email
             request.session['otp']=otp
             request.session['time']=str(datetime.now().time())
        
        
             return render(request, 'otp.html',{'phone':phone[-3:]})
       
    return render(request, 'base.html')

def resend(request):
    phone=request.session['phone']
    email=request.session['email']
    otp=''.join(random.choice(string.digits) for x in range(4))
    print(otp)
    try:
        mail='your otp is to visit '+otp+' Apply Procedures'
        send_mail('One Time Password', mail, 'feepayportal@gmail.com' ,[email], fail_silently=False)
    except gaierror:
                print('oops')
    client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    message = client.messages.create(
                                        messaging_service_sid='MG7b8f86e6946c32ae3229d0859b794d89', 
                                        body=f'Hi, your feepay otp is {otp}. Please enter this otp within 1 minute',
                                        to="+91"+phone 
                                        #to="+916362037635

                                    )
    print(message.sid)
    request.session['otp']=otp
    request.session['time']=str(datetime.now().time())
    return render(request, 'otp.html',{'phone':phone[-3:]})
    


def verification(request):
    if request.method=='POST':
        first=request.POST['first']
        second=request.POST['second']
        third=request.POST['third']
        fourth=request.POST['fourth']
        user_otp=first+second+third+fourth
        username=request.session['username']
        phone=request.session['phone']
        password1=request.session['password1']
        email=request.session['email']
        otp=request.session['otp']
        print(request.session['time'])
        #otptime=datetime.strptime(request.session['time'], '%H:%M:%S').time()
        otptime=dateutil.parser.parse(request.session['time'])
        print(otptime)
        
        if(datetime.now() <= otptime+ timedelta(minutes=1)):
            if user_otp==otp:
                user_obj=Account.objects.create_user(username=username, phone=phone, email=email, password=password1)
                user_obj.save()
                messages.success(request, 'user name created')   
                return render(request,'base.html')
            else:
                wrong_otp="Oops!! seems like your OTP is incorrect...please check the OTP"
                return render(request, 'otp.html',{'wrong_otp':wrong_otp})
        else:
                wrong_otp="Time expired!!!"
                return render(request, 'otp.html',{'Timeup':wrong_otp})
              

def log_in(request):
    #logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = encrypt(request.POST['password'])
        print(password)
        if(Account.objects.filter(username=username).exists() or Account.objects.filter(email=username).exists()):
            if(Account.objects.filter(username=username).exists()):
                 user = Account.objects.get(username=username)
            else:
                 user = Account.objects.get(email=username)
            if (user.check_password(password)):
                login(request, user)
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                site=site_settings.objects.get()
                conc=set_concession.objects.all()
                cllegeInfo=setCllegeInfo.objects.get()
                return render(request,'home.html',{'context':site,'conc1':conc[0].percentage_concession,'conc2':conc[1].percentage_concession,'conc3':conc[2].percentage_concession,'clg':cllegeInfo})

            else:
                messages.error(request, 'Invalid password')
              
        else:
                messages.error(request, 'Username is not registered')


    return render(request,'base.html')



def about_us(request):
    return render(request,'about.html')


@requires_csrf_token   
def password_reset_request(request):

	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
            
			associated_users = Account.objects.filter(Q(email=data))
			if associated_users.exists():
     
				for user in associated_users:
                  
					    subject = "Password Reset Requested"
					    email_template_name = "password/password_reset_email.txt"
					    c = {
					    "email":user.email,
					    'domain':'127.0.0.1:8000',
					    'site_name': 'Website',
					    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
					    "user": user,
					    'token': default_token_generator.make_token(user),
					    'protocol': 'http',
					    }
					    email = render_to_string(email_template_name, c)
					    try:
						    send_mail(subject, email, 'feepayportal@gmail.com' , [user.email], fail_silently=False)
                       
					    except BadHeaderError:
						    return HttpResponse('Invalid header found.')
					    return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

@login_required
def log_out(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    site=site_settings.objects.get()
    conc=set_concession.objects.all()
    cllegeInfo=setCllegeInfo.objects.get()
    return render(request,'home.html',{'context':site,'conc1':conc[0].percentage_concession,'conc2':conc[1].percentage_concession,'conc3':conc[2].percentage_concession,'clg':cllegeInfo})

          








          