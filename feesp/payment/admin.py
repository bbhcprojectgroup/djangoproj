from django.contrib import admin
from payment.models import Transaction
from login.admin import ac_site, DontLog

# Register your models here.
class TransactionAdmin(DontLog,admin.ModelAdmin):
    list_display=('user_mail','made_on', 'amount', 'order_id','status')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

#fd_site=accAdmin(name='Administration')

ac_site.register(Transaction,TransactionAdmin)


