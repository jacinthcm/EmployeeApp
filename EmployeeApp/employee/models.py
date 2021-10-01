from django.db import models


class Employee(models.Model):
    code = models.CharField(max_length=200, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    department = models.CharField(max_length=200, null=False, blank=False)
    age = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
