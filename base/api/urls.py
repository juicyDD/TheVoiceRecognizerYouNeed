from django.urls import path 
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('speaker-embedding/',views.getSpeakerEmbedding,name='speaker-embedding'),
    path('voices-similarity/', views.getSimilarityOfVoices,name='voices-similarity'),
    path('model-list/', views.getModels,name='model-list')
    #path('login/',views.LoginAPIView.as_view()),
]