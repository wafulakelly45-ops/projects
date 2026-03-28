from django.contrib.auth.models import AbstractUser
from django.db import models


# user model      
class User(AbstractUser):
     id = models.BigAutoField(primary_key=True)
      
   # model for the category 
class category(models.Model):
    id = models.BigAutoField(primary_key=True)
    category= models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"


# model for the listing

class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    Name=models.CharField(max_length=64)
    cover=models.ImageField(upload_to="images/", null=True,blank=True)
    Starting_Bid =models.IntegerField()
    Description = models.CharField(max_length=300)
    isActive =models.BooleanField()
    category= models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    Lister =models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name="User")

    
    def __str__(self):
        return f"{self.Name}:{self.cover} to {self.Starting_Bid} to {self.Description}"
  



