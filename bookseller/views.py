from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from myapp.models import *
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib import messages

# create your views here

def HOME(request):
    category = Category.objects.all()
    author = Author.objects.all()
    book = Book.objects.all()
    some_category = Category.objects.all().order_by('id')[0:8]
    data = {
        "category" : category,
        "author" : author,
        "book" : book,
        "some_category": some_category
    }
    return render(request, 'main/home.html', data)

def BOOK_DETAILS(request,slug):
    book = get_object_or_404(Book, slug=slug)
    all_books = Book.objects.all().order_by('-id')
    data={
        "book": book,
        "all_books": all_books
    }
    return render(request, 'details/book_details.html', data)

def AUTHOR_DETAILS(request,slug):
    author = get_object_or_404(Author, slug=slug)
    all_books = Book.objects.filter(author=author)
    data ={
        "author": author,
        "all_books": all_books
    }
    return render(request, 'details/author_details.html', data)

def CONTACT_US(request):      


    if request.method == "POST":
        pname = request.POST.get('name')
        pcompany = request.POST.get('company')
        pemail = request.POST.get('email')
        pmobile = request.POST.get('mobile')
        pmessage = request.POST.get('message')
        try:
            EmailMessage(
                'Contact form submission from {}'.format(pname), pmessage,
                'saurabh914691@gmail.com',
                # [],
                # [],
                reply_to=[pemail]
            ).send()
            pass_data = Contact(name=pname, email=pemail, company=pcompany, mobile=pmobile,message=pmessage)
            pass_data.save()
            messages.success(request, 'Message sent successfully ....!')
            return redirect('contact_us')
        except:
            pass
    return render(request, 'main/contact_us.html')


def ABOUT_US(request):
    return render(request, 'main/about_us.html')


def MY_CART(request):
    return render(request, 'orders/my_cart.html')