from django.db import models
from login.models import Account
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.core.mail import send_mail
from socket import gaierror
from django.shortcuts import render


# Create your models here.

COURSE_LIST = (
   ('BCA', 'BCA'),
   ('BCOM', 'BCom'),
   ('BSc', 'BSc'),
   ('BBA', 'BBA')
)

class crslist(models.Model):
    course = models.CharField(max_length=10, choices=COURSE_LIST)
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

class eccfee(models.Model):
    Libraryfee=models.IntegerField()
    Examfee=models.IntegerField()
    Associationfee=models.IntegerField()
    magzinefee=models.IntegerField()
    annualday=models.IntegerField()
    MUsportsfee=models.IntegerField()
    Admissionfee=models.IntegerField()
    sportfee=models.IntegerField()
    libraryfine=models.IntegerField()
    def __str__(self):
        return "eccfee"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'eccfee'
        verbose_name = 'Set ECC Fee'


class clgfeepaid(models.Model):
    email=models.EmailField(verbose_name="email",max_length=200, unique=True)
    name=models.CharField(max_length=30, default="xyz")
    roll_no=models.CharField(max_length=10)
    course=models.CharField(max_length=10)
    year=models.IntegerField(default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)])
    amount_paid= models.DecimalField(max_digits=10, decimal_places=2)
    receipt_image=models.FileField(upload_to='cllegeReceipts/', blank=True, null=True)
    date_of_fee=models.DateTimeField(default=timezone.now)
    transaction_id=models.CharField(max_length=100,null=True, blank=True)
    
    def __str__(self):
        return self.roll_no

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'clgpaid'
        verbose_name = 'Students who have paid full clg fee'


class clghalffeepaid(models.Model):
    email=models.EmailField(verbose_name="email",max_length=200, unique=True)
    name=models.CharField(max_length=30, default="xyz")
    roll_no=models.CharField(max_length=10)
    course=models.CharField(max_length=10)
    year=models.IntegerField(default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)])
    amount_paid= models.DecimalField(max_digits=10, decimal_places=2)
    receipt_image=models.FileField(upload_to='cllegeReceipts/', blank=True, null=True)
    date_of_fee=models.DateTimeField(default=timezone.now)
    transaction_id=models.CharField(max_length=100,null=True, blank=True)
    
    def __str__(self):
        return self.roll_no

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'clghalfpaid'
        verbose_name = 'Students who have paid half clg fee'


APPROVAL = (
   ('A', 'Accept'),
   ('R', 'Reject')
)

class concession_application(models.Model):
    email=models.EmailField(verbose_name="email",max_length=200, unique=True)
    name=models.CharField(max_length=30, default="xyz")
    roll_no=models.CharField(max_length=10)
    course=models.CharField(max_length=10)
    year=models.IntegerField(default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)])
    typeOfconcession=models.CharField(max_length=70,blank=True,null=True)
    document=models.FileField(upload_to='concreceipts/',null=True,blank=True)
    approve=models.CharField(choices=APPROVAL, max_length=128,default=None,null=True,blank=True)
    date_of_application=models.DateTimeField(default=timezone.now,null=True,blank=True)
    Reason_for_Rejection=models.CharField(max_length=100,default="None",null=True,blank=True)
    
    def save(self, *args, **kwargs):
        try:
            if self.approve=='A':

                send_mail('Concession Approved', 'your application for concession has been approved, Login to the feepay portal and pay your acadamic fee at concessioned rate. ' ,'feepayportal@gmail.com',[self.email], fail_silently=False)
            elif self.approve=='R':
                reject_reason=self.Reason_for_Rejection
                send_mail('Concession Rejected',reject_reason+'. your application for concession has been Rejected, Login to the feepay portal and kindly pay your full acadamic fee.The reason for rejection is' ,'feepayportal@gmail.com',[self.email], fail_silently=False)
            return super().save(*args, **kwargs)
        except gaierror:
                print("No Internet")
        
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'concession_application'
        verbose_name = 'View Concession application'


class set_concession(models.Model):
    concession_type=models.CharField(max_length=30, default="xyz")
    percentage_concession=models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.concession_type

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'concession_prcntage'
        verbose_name = 'Set Concession'

