from django.db import models

# Create your models here.
class Buyer(models.Model):
    id=models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,null=False)
    password = models.CharField(max_length=255,null=False)
    

class Seller(models.Model):
    id = models.AutoField(primary_key=True)  # Adding the id field
    username = models.CharField(max_length=255,null=False)
    password = models.CharField(max_length=255,null=False)
    

class Item(models.Model):
    id = models.AutoField(primary_key=True)  # Adding the id field
    itemname= models.CharField(max_length=255)
    description = models.CharField(max_length=900)
    itemproducer= models.ForeignKey(Seller, on_delete=models.CASCADE,null=True)
    
