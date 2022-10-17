import uuid
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser , AbstractUser)
from .manager import UserManager
from django.conf import settings
# from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
# from django.db.models.signals  import post_save , post_init
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    def random_otp():
        import random
        return str(random.randint(1000,9999))

    name = models.CharField(max_length=36)
    is_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    mobile = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Bus(models.Model):
    Number = models.CharField(max_length=10)
    seats = models.IntegerField( validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ])
    AC = models.BooleanField(default=True)

class Route(models.Model):

    class RouteList(models.TextChoices):
        UNA = 'Un', _('Una')
        HAROLI = 'HL', _('Haroli')
        GHALUWAL = 'GL', _('Ghaluwal')
        GAGRET = 'GG', _('Gagret')
        HOSHIARPUR = 'HR', _('Hoshiarpur')

    route = models.CharField(
        max_length=2,
        choices=RouteList.choices,
        default=RouteList.UNA,
    )

    def is_upperclass(self):
        return self.route in {
            self.YearInSchool.UNA,
            self.YearInSchool.HOSHIARPUR,
        }

class Ticket(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    passenger = models.OneToOneField(User,on_delete=models.CASCADE)
    fare = models.FloatField(help_text='Insert Reasonable Price')
    number = models.CharField(max_length=4)
    route = models.ManyToManyField(to=Route, related_name='routes')


