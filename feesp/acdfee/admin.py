from django.contrib import admin
from acdfee.models import crslist,clgfeepaid,clghalffeepaid,eccfee,set_concession,concession_application
from login.admin import ac_site, DontLog
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from datetime import datetime, timedelta, date
# Register your models here.
class eccfeeAdmin(DontLog,admin.ModelAdmin):
    list_display=('Libraryfee','Examfee','Associationfee','magzinefee','annualday','MUsportsfee','Admissionfee','sportfee','libraryfine')

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class clgfeepaidAdmin(DontLog,admin.ModelAdmin):
    list_display=('name','roll_no','course','year','amount_paid')
    search_fields=('roll_no',)

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class clghalffeepaidAdmin(DontLog,admin.ModelAdmin):
    list_display=('name','roll_no','course','year','amount_paid')
    search_fields=('roll_no',)

    actions = ['send_installment_mail',]

    @admin.action(description='Send reminder for second installment')
    def send_installment_mail(self, request, queryset):
        due=(date.today() +timedelta(days=30)).strftime("%d-%m-%Y")
        for i in queryset:
             obj=model_to_dict(i)
             email=obj['email']
             print(email)
             send_mail('Second Installment reminder', 'your second installment should be paid soon!!!Kindly pay your fee within '+str(due) ,'feepayportal@gmail.com',[email], fail_silently=False)

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class crslistAdmin(DontLog,admin.ModelAdmin):
    list_display=('course','year','fee')

class concessionAdmin(DontLog,admin.ModelAdmin):
    list_display=('email','name','course','year','typeOfconcession','approve')
    readonly_fields = ('email', 'name','roll_no','course','year','typeOfconcession','document','date_of_application')
    def has_add_permission(self, request):
        return False
class setconcessionAdmin(DontLog,admin.ModelAdmin):  
    list_display=('concession_type','percentage_concession') 
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


ac_site.register(set_concession,setconcessionAdmin)
ac_site.register(concession_application,concessionAdmin)
ac_site.register(clgfeepaid,clgfeepaidAdmin)  
ac_site.register(clghalffeepaid,clghalffeepaidAdmin)
ac_site.register(crslist,crslistAdmin)
ac_site.register( eccfee,eccfeeAdmin) 
    
    