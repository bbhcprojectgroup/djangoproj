from django.shortcuts import render
from django.http import HttpResponse
from acdfee.models import crslist,clgfeepaid,clghalffeepaid
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from json import dumps,loads
from django.forms.models import model_to_dict




def clgform(request):
    print('clgfee')
    cfee=crslist.objects.all()
    courses=[]
    for x in cfee:
        courses.append(model_to_dict(x))

    c_json=dumps(courses)
    global msg
    print(request.user.email)
    if(clgfeepaid.objects.filter(email=request.user.email).exists()):
        usr=clgfeepaid.objects.get(email=request.user.email)
        user=model_to_dict(usr)
        msg="fullpaid"
    elif(clghalffeepaid.objects.filter(email=request.user.email).exists()):
        usr=clghalffeepaid.objects.get(email=request.user.email)
        user=model_to_dict(usr)
        msg="halfpaid"

    else:
        user=None
        msg="notpaid"
    pass_cfee={'listyear':c_json,'user':user,'msg':msg}
    return render(request, 'acad.html',pass_cfee)

def clgfee(request):
    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['emailid']
        course=request.POST['course']
        rollno=request.POST['roll-no']
        clss=request.POST['year']
        if (msg=="halfpaid"):
            usr=clghalffeepaid.objects.get(email=request.user.email)
            amtpaid=float(usr.amount_paid)+float(request.POST['amt'])
        else:
            amtpaid=request.POST['amt']
        global data1
        global data
        global half
        data1=clghalffeepaid(name=name,email=email,course=course,year=clss,roll_no=rollno,amount_paid=amtpaid)
        data=clgfeepaid(name=name,email=email,course=course,year=clss,roll_no=rollno,amount_paid=amtpaid)
        print(request.POST['half'])
        if (request.POST['half']=="half"):
            print("half")
            half=True
            
        else:
            print("full")
            half=False
            
         
    return render(request, 'payclg.html')

def saveacad(request):
    if(half==True):
        if(clghalffeepaid.objects.filter(email=request.user.email).exists()):
            user = clghalffeepaid.objects.get(email=request.user.email)
            user.delete()
            data.save()
        else:
            data1.save()
    else:
        data.save()
    return render(request, 'home.html')