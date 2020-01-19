from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    #addtional
    
    def __str__(self):
        return self.user.username

# Create your models here.
class UserRequests(models.Model):
     
      username = models.CharField(blank=True,max_length=50)
      requests = models.CharField(blank=True,max_length=1000)
      
      def __str__(self):
        return self.username