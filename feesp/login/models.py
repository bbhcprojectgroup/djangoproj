

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager





# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not phone:
            raise ValueError("Users must have a contact no")

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,phone,password):
        user=self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            phone=phone,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

    def __str__(self):
        return self.email

class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name="email",max_length=60, unique=True)
    username=models.CharField(max_length=30,unique=True)
    date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    phone=models.CharField(max_length=30)
    

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','phone']

    objects=MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    class Meta:
        db_table = 'account_account'
        verbose_name = 'Account List'


class setCllegeInfo(models.Model):
    president_name=models.CharField(max_length=30)
    president_info=models.TextField()
    president_image=models.ImageField(upload_to='cllegeInfo/',null=True,blank=True)
    principal_name=models.CharField(max_length=30,null=True,blank=True)
    principal_info=models.TextField(null=True,blank=True)
    principal_image=models.ImageField(upload_to='cllegeInfo/',null=True,blank=True)
    vice_principal_name=models.CharField(max_length=30,null=True,blank=True)
    vice_principal_info=models.TextField(null=True,blank=True)
    vice_principal_image=models.ImageField(upload_to='cllegeInfo/',null=True,blank=True)
    principal_sign=models.ImageField(upload_to='cllegeInfo/',null=True,blank=True)
    clerk_sign=models.ImageField(upload_to='cllegeInfo/',null=True,blank=True)
    


    class Meta:
        db_table = 'CllegeInfo'
        verbose_name = 'College Information'

    def __str__(self):
        return "True"

    def has_perm(self, perm, obj=None): 
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
        
