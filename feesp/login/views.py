from django.shortcuts import render,redirect
from django.http import HttpResponse
from typing import cast
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from login.models import Account
from django.utils import timezone

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'home.html')

"""def feedback(request):
    return render(request,'feedback.html')"""

def about_us(request):
    return render(request,'about.html')

@requires_csrf_token   
def register(request):
    if (request.method =='POST'):
         username=request.POST['username']
         phone=request.POST['phone']
         email=request.POST['email']
         password1=request.POST['password']
         user = Account.objects.create_user(username=username, phone=phone, email=email, password=password1)
         user.save()
         #request.session['username'] = user.username
         messages.success(request, 'user name created')   
    return render(request,'base.html')
              


    


    


def log_in(request):
    #logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if(Account.objects.filter(username=username).exists()):
           user = Account.objects.get(username=username)
           if user.check_password(password):
                login(request, user)
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                return render(request,'home.html')
           else:
                messages.error(request, 'Invalid password')
                return redirect('/') 
        else:
                messages.error(request, 'Username is not registered')
                return redirect('/')    

    return render(request,'base.html')




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
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

@login_required
def log_out(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request,'base.html')
          