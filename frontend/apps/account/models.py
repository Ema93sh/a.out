from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userData(models.Model):
   user=models.OneToOneField(User) 
   ranking= models.IntegerField()
   #add other data here