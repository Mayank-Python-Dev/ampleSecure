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


class User(BaseModel, AbstractUser):
    email = models.EmailField(unique=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    phone_number = PhoneNumberField(region="IN", null=True, blank=True)
    city = models.CharField(max_length=128,null=True, blank=True,default="")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()

    class Meta:
        verbose_name_plural = _('User')

    def __str__(self):
        return self.email


class SuperUserManager(UserManager):
    # def create_user(self, email, password, **extra_fields):
    #     if not email or len(email) <= 0:
    #         raise ValueError("Email field is required !")
    #     if not password:
    #         raise ValueError("Password is must !")
    #     email = email.lower()
    #     user = self.model(
    #         email=email
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def get_queryset(self):
        return super(SuperUserManager, self).get_queryset().filter(
            groups__name='Super Admin')


class SuperUser(User):
    objects = SuperUserManager()
    class Meta:
        proxy = True
        verbose_name_plural= 'Super User'
    
    # def save(self, *args, **kwargs):
    #     return super().save(*args, **kwargs)


class AdminManager(UserManager):
    # def create_user(self, email, password, **extra_fields):
    #     if not email or len(email) <= 0:
    #         raise ValueError("Email field is required !")
    #     if not password:
    #         raise ValueError("Password is must !")
    #     email = email.lower()
    #     user = self.model(
    #         email=email
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def get_queryset(self):
        return super(AdminManager, self).get_queryset().filter(
            groups__name='Admin')


class Admin(User):
    objects = AdminManager()
    class Meta:
        proxy = True
        verbose_name_plural= 'Admin'


class RiskCoordinatorManager(UserManager):
    # def create_user(self, email, password, **extra_fields):
    #     if not email or len(email) <= 0:
    #         raise ValueError("Email field is required !")
    #     if not password:
    #         raise ValueError("Password is must !")
    #     email = email.lower()
    #     user = self.model(
    #         email=email
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def get_queryset(self):
        return super(RiskCoordinatorManager, self).get_queryset().filter(
            groups__name='Risk Coordinator')


class RiskCoordinator(User):
    objects = RiskCoordinatorManager()
    class Meta:
        proxy = True
        verbose_name_plural= 'Risk Co-Ordinator'


class FieldExecutiveManager(UserManager):
    # def create_user(self, email, password, **extra_fields):
    #     if not email or len(email) <= 0:
    #         raise ValueError("Email field is required !")
    #     if not password:
    #         raise ValueError("Password is must !")
    #     email = email.lower()
    #     user = self.model(
    #         email=email
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def get_queryset(self):
        return super(FieldExecutiveManager, self).get_queryset().filter(
            groups__name='Field Executive')


class FieldExecutive(User):
    objects = FieldExecutiveManager()
    class Meta:
        proxy = True
        verbose_name_plural= 'Field Executive'


class ClientManager(UserManager):
    # def create_user(self, email, password, **extra_fields):
    #     if not email or len(email) <= 0:
    #         raise ValueError("Email field is required !")
    #     if not password:
    #         raise ValueError("Password is must !")
    #     email = email.lower()
    #     user = self.model(
    #         email=email
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def get_queryset(self):
        return super(ClientManager, self).get_queryset().filter(
            groups__name='Client')


class Client(User):
    objects = ClientManager()
    class Meta:
        proxy = True
        verbose_name_plural= 'Client'


class SuperAdminAndAdminManager(UserManager):
    # def create_user(self, email, password, **extra_fields):
    #     if not email or len(email) <= 0:
    #         raise ValueError("Email field is required !")
    #     if not password:
    #         raise ValueError("Password is must !")
    #     email = email.lower()
    #     user = self.model(
    #         email=email
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def get_queryset(self):
        return super(SuperAdminAndAdminManager, self).get_queryset().filter(
            groups__name__in=['Super Admin','Admin'])


class SuperAdminAndAdmin(User):
    objects = SuperAdminAndAdminManager()
    class Meta:
        proxy = True
        verbose_name_plural= 'Super Admin & Admin'