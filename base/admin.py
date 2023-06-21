from django.contrib import admin
from .models import Post, UserToken
from django.contrib import admin
# Register your models here.


model_list = [Post, UserToken]
admin.site.register(model_list)
