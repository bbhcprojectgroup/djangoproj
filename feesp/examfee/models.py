from django.db import models
from login.models import Account
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.
class sublist(models.Model):
    sub_code=models.CharField(max_length=30,primary_key=True)
    subject=models.CharField(max_length=30)
    course=models.CharField(max_length=10)
    sem=models.IntegerField(default=1,
        validators=[MaxValueValidator(6), MinValueValidator(1)])
    optional=models.BooleanField(default=False)
    fee=models.IntegerField()
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
    name=models.CharField(max_length=30, default="xyz")
    roll_no=models.CharField(max_length=10)
    register_no=models.CharField(max_length=10, default="m")
    course=models.CharField(max_length=10)
    sem=models.IntegerField(default=1,
        validators=[MaxValueValidator(6), MinValueValidator(1)])
    amount_paid= models.DecimalField(max_digits=10, decimal_places=2)
    form_image=models.FileField(upload_to='examForms/', blank=True)
    receipt_image=models.FileField(upload_to='examReceipts/',null=True,blank=True)
    date_of_fee=models.DateTimeField(default=timezone.now)
    month=models.CharField(max_length=10,blank=True)
    college_code=models.CharField(max_length=10,blank=True)

    def __str__(self):
        return self.register_no

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'Exampaid'
        verbose_name = 'Students who have paid exam fee'



SEMESTER_CHOICES = (
   ('O', 'Odd'),
   ('E', 'Even')
)

class association(models.Model):
    Association=models.CharField(max_length=50)

    def __str__(self):
        return self.Association

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'Associations'
        verbose_name = 'Association list'

class site_settings(models.Model):
    siteEnable=models.BooleanField(verbose_name="Enable students to pay examination fee?",default=True)
    semester = models.CharField(choices=SEMESTER_CHOICES, max_length=128)
    marks_card_fee=models.IntegerField(default=1)
    Application_fee=models.IntegerField(default=1)


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'SiteStatus'
        verbose_name = 'Set options for exam fees payment'
