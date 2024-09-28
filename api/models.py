from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

Phone_Regex = RegexValidator(
    regex=r'^\d{10}$', message="Phone number must have 10 digits")

Name_Regex = RegexValidator(
    regex=r'^[a-zA-Z\s]*$', message="Name should only contain letters and spaces")


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone Number is required")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=250,validators=[Name_Regex],verbose_name="First Name")
    last_name = models.CharField(max_length=250,validators=[Name_Regex],verbose_name="Last Name")
    phone_number = models.BigIntegerField(validators=[Phone_Regex], unique=True,verbose_name="Phone Number")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name' ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        ordering = ['first_name','last_name']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    




class Tasks(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="User")
    title=models.CharField(max_length=50,verbose_name="Title")
    description=models.TextField(verbose_name="Description")
    due_date=models.DateTimeField(verbose_name="Due Date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False) 

    def __str__(self) -> str:
        return f'{self.user.full_name} {self.title}'