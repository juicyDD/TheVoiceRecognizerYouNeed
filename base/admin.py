from django.contrib import admin
from .models import Post
from django.contrib import admin
# Register your models here.
from .models import Post


model_list = [Post]
admin.site.register(model_list)
