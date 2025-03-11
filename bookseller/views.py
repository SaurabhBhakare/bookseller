from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from myapp.models import *
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from cart.cart import Cart

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
    book = Usercart.objects.all()
    if request.user.is_authenticated:
        cart_items = Usercart.objects.filter(user=request.user)
        total_price = sum(item.get_total_price() for item in cart_items)
        contex = {
            'book': book,
            'total_price': total_price,
        }
        return render(request, 'orders/my_cart.html',contex)
    else:
        return redirect('login_required')


def ADD_CART(request,slug):
    book = Book.objects.get(slug=slug)
    if request.user.is_authenticated:
        if Usercart.objects.filter(user=request.user, book=book).exists():
            usercart = Usercart.objects.get(user=request.user, book=book)
            usercart.quantity += 1
            usercart.save()
            messages.success(request, 'Book Quantity Updated.....!')
        else:
            usercart = Usercart(
                user=request.user,
                book=book,
                quantity='1',
            )
            usercart.save()
            messages.success(request, 'Book Added To Cart Successfully ....!')
        return redirect('my_cart')
    contex = {
            'book': book,
        }
    return render(request, 'orders/my_cart.html', contex)

def REMOVE_CART(request, book_id):
    if request.user.is_authenticated:
        book = Usercart.objects.get(book_id=book_id)
        book.delete()
        messages.warning(request, 'Book Remove From Cart Successfully ....!')
        return redirect('my_cart')
    contex = {
            'book': book,
        }
    return render(request, 'orders/my_cart.html', contex)
    


def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', {})

    # Add or update the book in the cart
    if not request.user.is_authenticated:
        if str(book_id) in cart:
            cart[str(book_id)]['quantity'] += 1
            messages.success(request, 'Book Quantity Updated.....!')
        else:
            cart[str(book_id)] = {
                'title': book.title,
                'author': book.author.author_name,
                'price': str(book.price),
                'discount': str(book.discount),
                'quantity': 1,
            }
            messages.success(request, 'Book Added To Cart Successfully ....!')
        request.session['cart'] = cart
        return redirect('view_cart')
    

def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})

    # Remove the book from the cart
    if str(book_id) in cart:
        del cart[str(book_id)]
        messages.warning(request, 'Book Remove From Cart Successfully ....!')
        request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    # Calculate total price and prepare cart items
    total_price = 0
    for book_id, item in cart.items():
        sellprice = float(item['price'])
        sellprice = float(item['price']) - (float(item['price']) * float(item['discount'])/100)
        item['total_price'] = int(sellprice) * item['quantity']
        total_price += item['total_price']
        cart_items.append(item)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    if not request.user.is_authenticated:
        return render(request, 'orders/session_cart.html', context)
    # else:
    #     return redirect('login_required')
    # return render(request, 'orders/my_cart.html', context)


def LOGIN_REQUIRED(request):
    return render(request, 'registration/login_requierd.html')

def MY_BOOKS(request):
    if request.user.is_authenticated:
        book = Userbooks.objects.all()
        contex = {
            'book': book,
        }
        return render(request, 'orders/my_books.html', contex)
    else:
        return redirect('login_required')