from django.db import models

from rest_framework.response import Response
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,\
    BaseUserManager, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
import os
from django.dispatch import receiver
# from encounterapp.models.department import Department


REQUEST_CHOICES = (
    ("DeliveryPerson", ("DeliveryPerson")),
    ("DressManager", ("DressManager")),
    ("SchoolAdmin", ("SchoolAdmin")),
    ("SystemAdmin", ("SystemAdmin")),
)


class UserManager(BaseUserManager):
    def create_user(self, first_name, middle_name, last_name, email, phone_number,
                    password=None, is_active=False, is_staff=False, is_admin=False):
        if not first_name:
            raise ValueError(("User must have a First name."))

        if not last_name:
            raise ValueError(("User must have a Last name."))

        if not email:
            raise ValueError(("Users must have email address."))

        if not phone_number:
            raise ValueError(("Users must have Phone Number."))

        if not password:
            raise ValueError(("User must have a password."))

        user_obj = self.model(
            email=email
        )

        user_obj.first_name = first_name
        user_obj.middle_name = middle_name
        user_obj.last_name = last_name
        user_obj.phone_number = phone_number
        user_obj.password = password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, first_name, middle_name, last_name, email,
                         phone_number, password=None):
        self.create_user(first_name, middle_name, last_name, email,
                         phone_number, password, is_staff=False, is_admin=False, is_active=True)

    def create_superuser(self, first_name, middle_name, last_name, email,
                         phone_number, password=None):
        self.create_user(first_name, middle_name, last_name,
                         email, phone_number, password, is_staff=True, is_admin=True, is_active=True)


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50,
                                  validators=[RegexValidator(
                                      regex="((?=.*[a-z])(?=.*[A-Z]))|((?=.*[A-Z])(?=.*[a-z]))|(?=.*[a-z])|(?=.*[A-Z])"
                                  )])
    middle_name = models.CharField(max_length=50,
                                   blank=True, null=True)
    last_name = models.CharField(max_length=50,
                                 validators=[RegexValidator(
                                     regex="((?=.*[a-z])(?=.*[A-Z]))|((?=.*[A-Z])(?=.*[a-z]))|(?=.*[a-z])|(?=.*[A-Z])"
                                 )],)
    email = models.EmailField(max_length=50, unique=True, null=True)
    phone_number = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='profile/', blank=False, null=True,
                              default='profile/default.jpg')
    token = models.CharField(max_length=30, blank=True, null=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    usertype = models.CharField(
        choices=REQUEST_CHOICES, default="Admin", max_length=250)
    created_at = models.DateField(auto_now=True, null=True)
    update_password = True

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name',
                       'middle_name', 'last_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if (self.admin != 'True' and self.update_password):
            self.set_password(self.password)
        user = super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def full_name(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

