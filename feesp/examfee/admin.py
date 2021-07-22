from django.contrib import admin
from examfee.models import sublist,examfeepaid, site_settings, association
from login.admin import ac_site
# Register your models here.

class examfeepaidAdmin(admin.ModelAdmin):
    list_display=('roll_no','amount_paid')

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class sublistAdmin(admin.ModelAdmin):
    list_display=('sub_code','subject','fee')



class site_settingsAdmin(admin.ModelAdmin):
    list_display=('siteEnable','semester')
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
   

ac_site.register(examfeepaid,examfeepaidAdmin)
ac_site.register(sublist,sublistAdmin)
ac_site.register(site_settings,site_settingsAdmin)
ac_site.register(association)
