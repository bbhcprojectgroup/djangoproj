from django.contrib import admin
from examfee.models import sublist,examfeepaid
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
    change_list_template='admin/snippet.html'



ac_site.register(examfeepaid,examfeepaidAdmin)
ac_site.register(sublist,sublistAdmin)
