from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from django.urls import reverse
from django.template.defaultfilters import slugify 
from datetime import datetime
class Post(models.Model):
    title = models.CharField(max_length=1024,verbose_name='Post Title')
    topic = models.CharField(max_length=1024,verbose_name='Topic',default='')
    slug = models.CharField(max_length=1024,verbose_name='Slug',null=True,blank=True)
    thumbnail = models.ImageField(upload_to='',null=True, blank=True)
    body = RichTextUploadingField(verbose_name='Content')
    summary = models.TextField(verbose_name='Summary')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("document", kwargs={"slug":self.slug})
    def save(self, *args, **kwargs):  # new
        if self.slug is None:
            self.slug = slugify(self.topic)+"&"+slugify(self.title)
        return super().save(*args, **kwargs)