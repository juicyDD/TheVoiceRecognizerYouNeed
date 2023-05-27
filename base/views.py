from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from .models import Post

def loginPage(request):
    
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        context["username"]=username
        password = request.POST.get('password')
        next = request.GET.get('next')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next:
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid password')

    return render(request,'base/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')       

def home(request):
    # posts = Post.objects.all()
    # context = {"posts":posts}
    return render(request,'base/homepage.html')

def tableofcontent(request):
    return render(request,'base/content.html')

def document(request,slug):
    return render(request,'base/document.html')

@login_required(login_url='login')
def apiPage(request):
    return HttpResponse("api")