from django.shortcuts import render
from django.http import HttpResponse
from .models import site_settings,sublist,examfeepaid,association
from django.contrib.auth.decorators import login_required
from json import dumps,loads
from django.forms.models import model_to_dict

# Create your views here.

@login_required
def exform(request):
    site=site_settings.objects.get()
    assoc=association.objects.all()
    print(assoc)
    if(site.siteEnable==True):
        sub=sublist.objects.all()
        slist=[]
        for s in sub:
            if(site.semester=='E'):
                semlist=[2,4,6]
                if(s.sem%2==0):
                    slist.append(model_to_dict(s))

            else:
                semlist=[1,3,5]
                if(s.sem%2!=0):
                    slist.append(model_to_dict(s))
        sub_json=dumps(slist)
        pass_sem={'sem1':semlist[0],'sem2':semlist[1],'sem3':semlist[2],'listsub':sub_json,'associations':assoc}
        
        return render(request,'examform.html',pass_sem)
    else:
        return render(request,'home.html')


def savestud(request):
    if(request.method=='POST'):
        expaid=examfeepaid()
        expaid.email=request.POST['emailid']
        expaid.name=request.POST['studname']
        expaid.roll_no=request.POST['roll-no']
        expaid.register_no=request.POST['regNo']
        expaid.course=request.POST['course']
        expaid.sem=request.POST['sem']
        expaid.amount_paid=500
        expaid.save()
        return render(request,'home.html')

expaid=examfeepaid()

def myajaxtestview(request):
        
        expaid.email=request.POST['emailid']
        expaid.name=request.POST['name'].upper()
        expaid.roll_no=request.POST['roll-no']
        expaid.register_no=request.POST['regNo']
        expaid.course=request.POST['course']
        expaid.sem=request.POST['sem']
        x=request.POST['sub']
        expaid.month=request.POST['monthyear']
        expaid.college_code=request.POST['col_code']
        global extra
        extra=request.POST['assoc']
        global data
        data = loads(x)
        print(data)
        print(data[0])
        
        #return HttpResponse(dumps("success"))
        return render(request,'home.html')


def exprintform(request):
    
    add_fee=site_settings.objects.get()
    csem=data[0]['sem']
    print(csem)
    markfee=add_fee.marks_card_fee
    appfee=add_fee.Application_fee
    tot=0
    tot1=tot2=tot3=0
    for d in data:
        if(d['sem']==1 or d['sem']==2):
             tot1=tot1+d['fee']
        elif(d['sem']==3 or d['sem']==4):
             tot2=tot2+d['fee']
        else:
             tot3=tot3+d['fee']

    if(tot1!=0):
        tot=tot+tot1+markfee
    if(tot2!=0):
        tot=tot+tot2+markfee
    if(tot3!=0):
        tot=tot+tot3+markfee
  
    tot=tot+appfee
    expaid.amount_paid=tot
    print(tot)
    context={'obj':expaid,'subs':data,'mfee':markfee,'afee':appfee,'t1':tot1,'t2':tot2,'t3':tot3,'t':tot,'sem':csem,'my_assoc':extra}
    print(context)
    return render(request,'form.html',context)