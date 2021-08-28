from django.contrib import admin
from acdfee.models import crslist,clgfeepaid,clghalffeepaid
from login.admin import ac_site, DontLog
# Register your models here.

class clgfeepaidAdmin(DontLog,admin.ModelAdmin):
    list_display=('name','roll_no','course','amount_paid')

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class clghalffeepaidAdmin(DontLog,admin.ModelAdmin):
    list_display=('name','roll_no','course','amount_paid')

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class crslistAdmin(DontLog,admin.ModelAdmin):
    list_display=('course','year','fee')


ac_site.register(clgfeepaid,clgfeepaidAdmin)  
ac_site.register(clghalffeepaid,clghalffeepaidAdmin)
ac_site.register(crslist,crslistAdmin) 
    
    