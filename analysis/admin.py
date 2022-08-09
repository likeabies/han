from django.contrib import admin
from .models import User, Notices

# Register your models here.

admin.site.register(User)
admin.site.register(Notices)