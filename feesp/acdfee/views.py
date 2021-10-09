from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from acdfee.models import crslist,clgfeepaid,clghalffeepaid,eccfee,concession_application,set_concession
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from json import dumps,loads
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from login.models import setCllegeInfo
from weasyprint import HTML,CSS
import tempfile
import os
from feesp.settings import MEDIA_ROOT




@login_required
def clgform(request):
    print('clgfee')
    cfee=crslist.objects.all()
    courses=[]
    for x in cfee:
        courses.append(model_to_dict(x))
    global c_json
    c_json=dumps(courses)
    global msg
    print(request.user.email)
    """if(clgfeepaid.objects.filter(email=request.user.email).exists()):
        usr=clgfeepaid.objects.get(email=request.user.email)
        user=model_to_dict(usr)
        msg="fullpaid"""
    if(clghalffeepaid.objects.filter(email=request.user.email).exists()):
        usr=clghalffeepaid.objects.get(email=request.user.email)
        user=model_to_dict(usr)
        msg="halfpaid"

    else:
        user=request.user
        msg="notpaid"
    pass_cfee={'listyear':c_json,'user':user,'msg':msg}
    return render(request, 'acad.html',pass_cfee)

@login_required
def clgfee(request):


    if request.method =='POST':
        name=request.POST['name']
        email=request.POST['emailid']
        course=request.POST['course']
        rollno=request.POST['roll-no']
        clss=request.POST['year']
        global amtpaid
        global discount
        global totfee
        concstatus="None"
        discount=0
        if(clgfeepaid.objects.filter(email=email, year=clss).exists()):
            return render(request, 'acad.html',{'msg':"fullpaid",'listyear':c_json})
        else:
            amtpaid=float(request.POST['amt'])
            totfee=amtpaid
            global data1
            global data
            global half
            if(concession_application.objects.filter(email=email,year=clss).exists()):
                    apply_conc=concession_application.objects.get(email=email,year=clss)
                    if(apply_conc.approve=='A'):
                        concstatus="Approved"
                        conc_type=apply_conc.typeOfconcession
                        ex=set_concession.objects.get(concession_type=conc_type)
                        con_prct=float(ex.percentage_concession)
                        discount=con_prct*amtpaid/100
                        amtpaid=amtpaid-discount
                        print(amtpaid)         
                    elif(apply_conc.approve=='R'):
                        concstatus="Rejected"
                    else:
                        concstatus="waiting"

            if (msg=="halfpaid"):
                data1=clghalffeepaid(name=name,email=email,course=course,year=clss,roll_no=rollno,amount_paid=float(amtpaid)*2)
                data=clgfeepaid(name=name,email=email,course=course,year=clss,roll_no=rollno,amount_paid=float(amtpaid)*2)
        
            else:
                
                    
                    data1=clghalffeepaid(name=name,email=email,course=course,year=clss,roll_no=rollno,amount_paid=amtpaid)
                    data=clgfeepaid(name=name,email=email,course=course,year=clss,roll_no=rollno,amount_paid=amtpaid)

            print(request.POST['half'])
            if (request.POST['half']=="half"):
                print("half")
                half=True
   
            else:
                print("full")
                half=False       
        return render(request, 'payclg.html',context={'amnt':amtpaid,'data':data,'cstatus':concstatus})
@login_required
def saveacad(request,transid):
    data.transaction_id=transid
    data1.transaction_id=transid
    print(request.user.email)
    if(clgfeepaid.objects.filter(email=request.user.email).exists()):
        old_data=clgfeepaid.objects.get(email=request.user.email)
        old_data.delete()
    global Eccfee
    Eccfee=eccfee.objects.get()
    fee=int(float(totfee))
    feerem=fee-Eccfee.Libraryfee-Eccfee.Examfee-Eccfee.Associationfee-Eccfee.magzinefee-Eccfee.annualday-Eccfee.MUsportsfee-Eccfee.Admissionfee-Eccfee.sportfee-Eccfee.libraryfine
    clg=setCllegeInfo.objects.get()
    psign=clg.principal_sign
    csign=clg.clerk_sign
    if(half==True):
        if(clghalffeepaid.objects.filter(email=request.user.email).exists()):
            user = clghalffeepaid.objects.get(email=request.user.email)
            rno=user.roll_no
            user.delete()
            print(rno)
            if os.path.exists(MEDIA_ROOT + "/collegeReceipts/" +rno+".pdf"):
                os.remove(MEDIA_ROOT + "/collegeReceipts/" +rno+".pdf")
            html_string = render_to_string('re2.html',{'context':model_to_dict(data),'amt':amtpaid,'con':discount,'tot':totfee,'psign':psign,'csign':csign,'trans':transid}, request=request)
            html = HTML(string=html_string, base_url='request.build_absolute_uri()')
            result = html.write_pdf(presentational_hints=True)
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                #response.write(output.read())
                data.receipt_image.save(data.roll_no+".pdf",output)

            
            
        else:
            
            
            
            html_string = render_to_string('re.html',{'context':model_to_dict(data1),'ecfee':Eccfee,'tfee':feerem, 'amt':amtpaid,'con':discount,'tot':totfee,'psign':psign,'csign':csign,'trans':transid}, request=request)
            html = HTML(string=html_string, base_url='request.build_absolute_uri()')
            result = html.write_pdf(presentational_hints=True)
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                #response.write(output.read())
                data1.receipt_image.save(data.roll_no+".pdf",output)
            
    else:
       
        html_string = render_to_string('re.html',{'context':model_to_dict(data),'ecfee':Eccfee,'tfee':feerem, 'amt':amtpaid,'con':discount,'tot':totfee,'psign':psign,'csign':csign,'trans':transid}, request=request)
        html = HTML(string=html_string, base_url='request.build_absolute_uri()')
        result = html.write_pdf(presentational_hints=True)
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            #response.write(output.read())
            data.receipt_image.save(data.roll_no+".pdf",output)


    return render(request, 'home.html')

@login_required
def applyconc(request):
    email=request.POST['email']
    name=request.POST['name']
    course=request.POST['course']
    year=request.POST['year']
    rolno=request.POST['rlno']
    doc=request.FILES['file']
    conctype=request.POST['contype']

    if(concession_application.objects.filter(email=email,year=year).exists()):
        conobj=concession_application.objects.get(email=email,year=year)
        print(conobj)
        if(conobj.approve=='A'):
            msg="Your application has been approved,Proceed to pay your acadamic fees"

        elif(conobj.approve=='R'):
            msg="Your application for concession has been rejected, Kindly pay your full acadamic fees"

        else:
            msg="you have already applied for concession and is under process wait for confirmation mail"
        
    elif(clgfeepaid.objects.filter(email=email,year=year).exists()):
        msg="You have already paid your fees!!!"
    elif(clghalffeepaid.objects.filter(email=email,year=year).exists()):
        msg="You have paid your half fees!!! Cant apply for concession now"
        
    else:
        if(concession_application.objects.filter(email=email).exists()):
            oldobj=concession_application.objects.get(email=email)
            oldobj.delete()
        msg="Your application for concession has been submitted, confirmation mail would be sent soon!! to registered mail Id"
        conc=concession_application(name=name,email=email,course=course,year=year,roll_no=rolno,document=doc,typeOfconcession=conctype)
        conc.save()
    return render(request, 'concession.html',{'msg':msg,'user':request.user})



    

@login_required
def receipt(request):

    if(half==True and msg=="notpaid"):
        response = FileResponse(open(MEDIA_ROOT + "/"+str(data1.receipt_image), 'rb'))  
    else:
        response = FileResponse(open(MEDIA_ROOT + "/"+str(data.receipt_image), 'rb'))
    return response