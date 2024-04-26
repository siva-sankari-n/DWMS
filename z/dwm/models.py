from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class storecomplain(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
      name = models.CharField(max_length=25, blank=False, null=False)
      email = models.EmailField()
      complaint = models.CharField(max_length=500)
      locat = models.CharField(max_length=25, blank=False, null=False)
      locatd = models.CharField(max_length=500)

      class Meta:
            db_table="dwms_complaint"