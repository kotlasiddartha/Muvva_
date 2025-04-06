from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Receipe(models.Model):
    User = models.ForeignKey(User , on_delete=models.SET_NULL , null=True, blank=True)
    case_number = models.CharField(max_length=100, null=True, blank=True)
    receipe_name = models.CharField(max_length=100, null=True, blank=True)

    relation = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    family_history = models.TextField(null=True, blank=True)
    investigation = models.TextField(null=True, blank=True)
    

    receipe_description = models.TextField(null=True, blank=True)
    receipe_image = models.ImageField(upload_to="receipe")
    

