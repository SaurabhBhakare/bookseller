from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout  
from myapp.EmailBackEnd import EmailBackEnd

def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # For email validation
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exist')
            return redirect('register')
        # For username validation
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('register')
        user = User(email=email, username=username)
        user.set_password(password)
        user.save()
        return redirect('dologin')
    return render(request, 'registration/register.html')

def DOLOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if user != None:
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'Email or Password is Invalid !')
            return redirect('dologin')
    return render(request, 'registration/login.html')


def DOLOGOUT(request):
    logout(request)
    if not request.user.is_authenticated:
        return redirect('dologin')
    return render(request, 'main/home.html')