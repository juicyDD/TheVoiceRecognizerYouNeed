from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),
    path('documentation/<str:slug>/',views.document,name='document'),
    path('documentation',views.tableofcontent,name='table-content'),
    path('api',views.apiPage,name='api'),
]
