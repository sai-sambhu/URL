from django.contrib import admin
from basic_app.models import UserProfile,UserRequests

# Register your models here.
admin.site.register([UserProfile,UserRequests])
