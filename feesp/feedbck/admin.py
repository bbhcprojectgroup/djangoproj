
# Register your models here.
from django.contrib import admin
from feedbck.models import FeedBack
from login.admin import ac_site

# Register your models here.
class FeedbkAdmin(admin.ModelAdmin):
    list_display=('firstname','email','phone','feedback')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

#fd_site=accAdmin(name='Administration')

ac_site.register(FeedBack,FeedbkAdmin)