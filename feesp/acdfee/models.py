from django.db import models
from login.models import Account
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


# Create your models here.
class crslist(models.Model):
    course=models.CharField(max_length=10)
    year=models.IntegerField(default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)])
    fee=models.IntegerField()

    def __str__(self):
        return self.course

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'clgFee'
        verbose_name = 'course list'

class clgfeepaid(models.Model):
    email=models.EmailField(verbose_name="email",max_length=60, unique=True)
    name=models.CharField(max_length=30, default="xyz")
    roll_no=models.CharField(max_length=10)
    course=models.CharField(max_length=10)
    year=models.IntegerField(default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)])
    amount_paid= models.DecimalField(max_digits=10, decimal_places=2)
    receipt_image=models.ImageField(upload_to='examReceipts/',height_field='picture_height',width_field='picture_width',max_length=255,null=True,blank=True)
    date_of_fee=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'clgpaid'
        verbose_name = 'Students who have paid full clg fee'


class clghalffeepaid(models.Model):
    email=models.EmailField(verbose_name="email",max_length=60, unique=True)
    name=models.CharField(max_length=30, default="xyz")
    roll_no=models.CharField(max_length=10)
    course=models.CharField(max_length=10)
    year=models.IntegerField(default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)])
    amount_paid= models.DecimalField(max_digits=10, decimal_places=2)
    receipt_image=models.ImageField(upload_to='examReceipts/',height_field='picture_height',width_field='picture_width',max_length=255,null=True,blank=True)
    date_of_fee=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'clghalfpaid'
        verbose_name = 'Students who have paid half clg fee'

