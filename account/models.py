import uuid
from django.db import models
from .managers import UserManager
from django.utils.translation import gettext as _
from polymorphic.models import PolymorphicModel
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel,AbstractUser,PolymorphicModel):
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(unique=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()

    class Meta:
        verbose_name_plural = _('User')

    def __str__(self):
        return self.email

# # Polymorphic models for Client
# # Client models doesn't have first_name ,last_name & phone_number fields

class Client(User):
    company_name = models.CharField(max_length=256,default="",unique=True)

    class Meta:
        verbose_name_plural = _('Client')

class Admin(User):
    username = models.CharField(max_length=256,default="",unique=True)
    first_name = models.CharField(max_length=256,default="",unique=False)
    last_name = models.CharField(max_length=256,default="",unique=False)
    phone_number = PhoneNumberField(region="IN")

    class Meta:
        verbose_name_plural = _('Admin')


class SuperAdmin(User):
    username = models.CharField(max_length=256,default="",unique=True)
    first_name = models.CharField(max_length=256,default="",unique=False)
    last_name = models.CharField(max_length=256,default="",unique=False)
    phone_number = PhoneNumberField(region="IN")

    class Meta:
        verbose_name_plural = _('Super Admin')


class RiskCoordinator(User):
    username = models.CharField(max_length=256,default="",unique=True)
    first_name = models.CharField(max_length=256,default="",unique=False)
    last_name = models.CharField(max_length=256,default="",unique=False)
    phone_number = PhoneNumberField(region="IN")

    class Meta:
        verbose_name_plural = _('Risk Co-Ordinator')


class FieldExecutive(User):
    username = models.CharField(max_length=256,default="",unique=True)
    first_name = models.CharField(max_length=256,default="",unique=False)
    last_name = models.CharField(max_length=256,default="",unique=False)
    phone_number = PhoneNumberField(region="IN")

    class Meta:
        verbose_name_plural = _('Field Executive')

