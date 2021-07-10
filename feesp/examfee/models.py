from django.db import models
from login.models import Account
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class sublist(models.Model):
    sub_code=models.CharField(max_length=30,primary_key=True)
    subject=models.CharField(max_length=30)
    course=models.CharField(max_length=10)
    sem=models.IntegerField(default=1,
        validators=[MaxValueValidator(6), MinValueValidator(1)])
    optional=models.BooleanField(default=False)
    fee=models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.subject

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'SubFee'
        verbose_name = 'Subject List'
    
class examfeepaid(models.Model):
    email=models.EmailField(verbose_name="email",max_length=60, unique=True)
    roll_no=models.CharField(max_length=10)
    course=models.CharField(max_length=10)
    sem=models.IntegerField(default=1,
        validators=[MaxValueValidator(6), MinValueValidator(1)])
    amount_paid= models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.subject

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'Exampaid'
        verbose_name = 'Students who have paid exam fee'
    
