from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import Post, UserToken
from .forms import SignUpForm
from knox.models import AuthToken 
from django.core import serializers
import json

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
        pw2=request.POST.get('password2')
        pw=request.POST.get('password')
        username_ = request.POST.get('username').lower()
        email_ = request.POST.get('email').lower()
        print(username_,email_)
        err_message_ = None
        
        status = 0
        usertemp1 = User.objects.filter(username=username_).count()
        usertemp2 = User.objects.filter(email=email_).count()
        print('count',usertemp1,usertemp2)
        if (usertemp1==0 and usertemp2==0) :
            status = 1 
        status += 2 if (usertemp1!=0 and usertemp2==0) else(-2 if usertemp1==0 and usertemp2 !=0 else 0)
        print('status',status)
        err = []
        if status == 2:
            err_message_ ='Username is already taken'
        elif status == -2:
            err_message_ ='Email is already taken'
        elif status == 0:
            err_message_ ='Email and username are already taken'
        if err_message_ :
            err.append(err_message_)
        if (pw!=pw2):
            err.append('Password mismatch')
        user = None
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            if status == 1:
                user.save()
                messages.success(request, "Registered successfully")        
        else:
            messages.error(request, '. '.join(err))
                
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
    context = {'post':post,'related_posts':related_posts}
    return render(request,'base/document.html',context)

@login_required(login_url='login')
def editUser(request):
    context = {'username':request.user.username,
               'first_name': request.user.first_name,
               'last_name': request.user.last_name,
               'email':request.user.email}
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        if request.user.username!=username and User.objects.filter(username=username).count() > 0:
            messages.error(request, 'This username has already been taken')
        else:
            myuser = User.objects.get(username=request.user.username)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.username = username
            myuser.save()
            context['first_name'] = firstname
            context['last_name'] = lastname
            context['username'] = username
            messages.success(request, 'Update successfully')
    return render(request, 'base/edit_user.html', context)

@login_required(login_url='login')
def apiPage(request):
    context = {}
    return render(request,'base/api_list.html',context)

@login_required(login_url='login')
def apiTokenList(request):
    tokens = UserToken.objects.filter(email=request.user.email)
    context = {'tokens': tokens,'token':None}
    if request.method == 'POST':
        apiname = request.POST.get('name')
        print(apiname)
        instance, token=AuthToken.objects.create(request.user)
            
        abb = token[:4] +"..." + token[-4:]
        expiry = instance.expiry
        context['token']=str(token)
        UserToken.objects.create(
            name = apiname,
            token_key = instance.token_key,
            email = request.user.email,
            abbreviation = abb,
            expiry =expiry
        )
        # _ = UserToken.objects.filter(token_key=instance.token_key).first()
        tokenlist_json = serializers.serialize('json', tokens)
        return JsonResponse({'token':str(token),
                             'token_key': str(instance.token_key),
                             'token_name':apiname,
                             'abbreviation':abb,
                             'expiry':expiry,
                             'tokens':tokenlist_json})
    return render(request,'base/api_token_list.html', context)

@login_required(login_url='login')
def deleteToken(request):
    if request.method == 'POST':
        token_key = request.POST.get('token_key')
        token = AuthToken.objects.get(token_key=token_key)
        if request.user !=token.user:
            return JsonResponse({'deleteMessage':'You are not allowed to delete this token'})
        token.delete()
        UserToken.objects.get(token_key=token_key).delete()
    return JsonResponse({'deleteMessage':'Token was successfully deleted'})