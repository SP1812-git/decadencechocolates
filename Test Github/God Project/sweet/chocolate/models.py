from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChocolateTable(models.Model):
   chocolate_id=models.AutoField(primary_key=True)
   chocolate_name=models.CharField(max_length=100)
   chocolate_price=models.IntegerField()
   chocolate_description=models.CharField(max_length=100)
   chocolate_quantity=models.IntegerField()
   chocolate_flavour=models.CharField(max_length=100)
   chocolate_weight=models.IntegerField()
   chocolate_event=models.CharField(max_length=100)
   chocolate_shape=models.CharField(max_length=100)
   image=models.ImageField(upload_to='image')
   is_available=models.BooleanField()

class CartTable(models.Model):
      #uid_id
      user_id = models.ForeignKey(User,on_delete=models.CASCADE,db_column='user_id')
      chocolate_id = models.ForeignKey(ChocolateTable,on_delete=models.CASCADE,db_column='chocolate_id')
      quantity=models.IntegerField() 
