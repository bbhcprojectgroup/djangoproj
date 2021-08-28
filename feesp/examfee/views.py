from django.shortcuts import render,redirect
from django.utils.timezone import localdate
import os
from django.http import FileResponse
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib import messages
from .models import site_settings,sublist,examfeepaid,association
from django.contrib.auth.decorators import login_required
from json import dumps,loads
from django.forms.models import model_to_dict
from examfee.utils import render_to_pdf
from django.template.loader import render_to_string
from weasyprint import HTML,CSS
import tempfile
from feesp.settings import MEDIA_ROOT



#for saving pdf
from django.core.files import File
from django.core.files.base import ContentFile
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO


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
        return render(request,'error.html')

"""def savestud(request):
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
        return render(request,'home.html')"""


expaid=examfeepaid()
@login_required
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
        
        return render(request,'home.html')

@login_required
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
    global context
    context={'obj':expaid,'subs':data,'mfee':markfee,'afee':appfee,'t1':tot1,'t2':tot2,'t3':tot3,'t':tot,'sem':csem,'my_assoc':extra, 'bton':True,'pdf':False}
    print(context)
    return render(request,'form.html',context)





"""def download_file(request, file_id):
    testfile = get_object_or_404(TestResultFile, pk=file_id)
    wrapper = FileWrapper(open(testfile.path, "r" ))
    response=HttpResponse(wrapper, content_type="text/plain")
    response['Content-Disposition'] ='attachment; filename="results.txt"'
    return response """


"""def download_file(request):
    pdf = render_to_pdf('form.html', context)
    if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download =request.POST.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
    return HttpResponse("Not found")"""






def download_file(request):
    print("download")
    context['bton']=False
    context['pdf']=True
    print(context['bton'])
    file_name=expaid.register_no+".pdf"
    response = FileResponse(open(MEDIA_ROOT + "/examForms/" + file_name, 'rb'))   
    return response



def save_sign(request):
           print("sign uploaded")
           context['bton']=False
           context['pdf']=False
           sign_image = request.FILES['signature']
           file_name = expaid.register_no+".png"
           print("file_name", file_name)
           print("content_type", sign_image.content_type)
           print("size", sign_image.size)
           with open(MEDIA_ROOT + "/" + file_name, 'wb+') as f:
                for chunk in sign_image.chunks():
                        f.write(chunk)                 
           return render(request,'form.html',context)
 
def data_save(request):
    if(examfeepaid.objects.filter(email=expaid.email).exists()):
        print("match found")
        user = examfeepaid.objects.get(email=expaid.email)
        user.delete()
    context['bton']=False
    context['pdf']=True
    html_string = render_to_string('form.html', context, request=request)
    html = HTML(string=html_string, base_url='request.build_absolute_uri()')
    result = html.write_pdf(presentational_hints=True)
    # Creating http response
    """response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=examform.pdf'
    response['Content-Transfer-Encoding'] = 'UTF-8'"""
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        #response.write(output.read())
        expaid.form_image.save(expaid.register_no+".pdf",output)
        if os.path.exists(MEDIA_ROOT + "/" + expaid.register_no+".png"):
            os.remove(MEDIA_ROOT + "/" + expaid.register_no+".png")
    return render(request,'paysuccess.html')    
   
