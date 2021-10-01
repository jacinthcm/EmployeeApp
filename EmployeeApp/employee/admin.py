from django.contrib import admin
from django.contrib.auth.models import User

from employee.models import Employee
# Register your models here.

admin.site.register(Employee)
