from msilib.schema import Class
from django.db import models

# Create your models here.


class CustomUser(models.Model):
        mobile = models.CharField("Mobile Number",max_length=200,blank=True,null=True)
        txnid =  models.CharField("txnid",max_length=200,blank=True,null=True)

 

class AbhaDetails(models.Model):
        user           = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True, blank=True)
        health_id        = models.CharField("Health Id",max_length=200,blank=True,null=True)
        token            = models.CharField("Token",max_length=400,blank=True,null=True)
        refreshtoken     = models.CharField("Token",max_length=400,blank=True,null=True)
        

