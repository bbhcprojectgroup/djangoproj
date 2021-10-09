from django.contrib import admin
from examfee.models import sublist,examfeepaid, site_settings, association
from login.admin import ac_site,DontLog
# Register your models here.

class examfeepaidAdmin(DontLog,admin.ModelAdmin):
    list_display=('name','roll_no','course','sem','register_no','amount_paid')
    search_fields=('register_no',)

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class sublistAdmin(admin.ModelAdmin):
    list_display=('sub_code','course','sem','subject','fee')
    search_fields=('sub_code',)




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
