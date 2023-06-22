from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),
    path('settings',views.editUser, name='edit-user'),
    path('documentation/<str:slug>/',views.document,name='document'),
    path('documentation',views.tableofcontent,name='table-content'),
    path('api-guidelines',views.apiPage,name='api'),
    path('api-tokens',views.apiTokenList,name='api-tokens'),
    path('delete-token', views.deleteToken,name='delete-token'),
    path('api/',include('base.api.urls'))
]
