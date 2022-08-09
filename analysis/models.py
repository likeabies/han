from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password, name, email, phone, date_of_birth):
        user = self.model(
            username=username,
            name=name,
            email=self.normalize_email(email),
            phone=phone,
            date_of_birth=date_of_birth,
            date_joined=timezone.now(),
            is_superuser=0,
            is_staff=0,
            is_active=1
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, email, phone, date_of_birth, password):
        user = self.create_user(
            username=username,
            password=password,
            name=name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth
        )
        user.is_superuser = 1
        user.is_staff = 1
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    username = models.CharField(unique=True, max_length=150)
    is_superuser = models.IntegerField()
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=254)
    date_of_birth = models.DateTimeField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
    is_staff = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone', 'email', 'date_of_birth']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'auth_user'
        
        # This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Notices(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    title = models.CharField(max_length=300)
    content = models.TextField()
    registered_date = models.DateTimeField(blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notices'
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Notices(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    title = models.CharField(max_length=300)
    content = models.TextField()
    registered_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notices'
