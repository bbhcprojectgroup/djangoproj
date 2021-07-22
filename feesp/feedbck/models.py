
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FeedBack(models.Model):
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    phone=models.CharField(max_length=11)
    email=models.EmailField(max_length=60, unique=True)
    feedback=models.CharField(max_length=1000)

    class Meta:
        db_table = 'feedb_table'
        verbose_name = 'feedback list'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None): 
        return self.is_admin

    def has_module_perms(self, app_label):
        return True