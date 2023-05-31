from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from .models import Post
from .forms import SignUpForm

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
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

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = SignUpForm()
    context = {'form':form}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # login(request, user)
            messages.success(request, "Registered successfully")
            # return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, "base/register.html",context)
def home(request):
    # posts = Post.objects.all()
    # context = {"posts":posts}
    return render(request,'base/homepage.html')

def tableofcontent(request):
    return render(request,'base/content.html')

def document(request,slug):
    post = Post.objects.filter(slug=slug)[0]
    related_posts = Post.objects.filter(topic=post.topic)
    context = {'post':post}
    return render(request,'base/document.html',context)



@login_required(login_url='login')
def apiPage(request):
    return HttpResponse("api list")