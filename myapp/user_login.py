from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout  
from myapp.EmailBackEnd import EmailBackEnd

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = request.build_absolute_uri(f'/verify-email/{uid}/{token}/')
    contex ={
        "verification_link": verification_link,
        "user": user,
    }

    html_message = render_to_string("registration/email_verification_template.html", contex)
    
    plain_message = strip_tags(html_message)

    subject = "Verify Your Email"
    DEFAULT_FROM_EMAIL = 'Bookseller.com'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # For email validation
        if User.objects.filter(email=email).exists() and User.objects.get(email=email).is_active == True:
            messages.warning(request, 'Email already exists')
            return redirect('register')
        elif User.objects.filter(email=email).exists() and User.objects.get(email=email).is_active == False:
            user = User.objects.get(email=email)
            messages.warning(request, 'Email not verified..! Check inbox')
            send_verification_email(request, user)
            return redirect('register')

        # For username validation
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('register')
        user = User(email=email, username=username)
        user.set_password(password)
        user.is_active = False
        user.save()

        send_verification_email(request, user)

        messages.success(request, "A verification email has been sent. Check inbox")
        return redirect('dologin')
    return render(request, 'registration/register.html')

def DOLOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if User.objects.filter(email=email).exists() and User.objects.get(email=email).is_active == False:
            user = User.objects.get(email=email)
            messages.warning(request, 'Email not verified..! Check inbox')
            send_verification_email(request, user)
            return redirect('dologin')
        elif user != None:
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



def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Email verification successful! You can now log in.")
        else:
            return HttpResponse("Invalid verification link.", status=400)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Invalid verification request.", status=400)
