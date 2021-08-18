

# Register your models here.
from django.contrib import admin
from login.models import Account

# Register your models here.

class DontLog:
    def log_addition(self, *args):
        return
    def log_change(self, *args):
        return
    def log_deletion(self, *args):
        return

class accAdmin(admin.AdminSite):
    pass


class AccntAdmin(DontLog,admin.ModelAdmin):
    list_display=('email','username','phone','is_active')


    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    

ac_site=accAdmin(name='Administration')

ac_site.register(Account,AccntAdmin)
