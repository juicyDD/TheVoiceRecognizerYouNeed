from django.urls import path 
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('speaker-embedding/',views.getSpeakerEmbedding,name='speakerEmbedding')
]