from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from myapp.models import *
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from cart.cart import Cart

import razorpay
from time import time
from django.views.decorators.csrf import csrf_exempt
from .settings import *

from myapp.utils import convert_pdf_to_images

secreate_key = settings.SECRET_KEY
secreate_id = settings.SECRET_ID


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
    if not book.pages.exists() and book.book_file:
        convert_pdf_to_images(book)

    pages = book.pages.all().order_by('page_number')
    all_books = Book.objects.all().order_by('-id')
    data={
        "book": book,
        "all_books": all_books,
        "pages": pages
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
    book = Usercart.objects.filter(user=request.user)
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
            messages.success(request, 'Book already exists in cart.....!')
        elif Userbooks.objects.filter(user=request.user, book=book).exists():
            messages.success(request, 'Book already exists in Mybooks.....!')
            return redirect("my_books")
        else:
            usercart = Usercart(
                user=request.user,
                book=book,
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
            messages.success(request, 'Book Already exists in Cart.....!')
        else:
            cart[str(book_id)] = {
                'title': book.title,
                'author': book.author.author_name,
                'price': str(book.price),
                'discount': str(book.discount),
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
        item['total_price'] = int(sellprice)
        total_price += item['total_price']
        cart_items.append(item)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    if not request.user.is_authenticated:
        return render(request, 'orders/session_cart.html', context)


def LOGIN_REQUIRED(request):
    return render(request, 'registration/login_requierd.html')

def MY_BOOKS(request):
    if request.user.is_authenticated:
        book = Userbooks.objects.filter(user=request.user)
        contex = {
            'book': book,
        }
        return render(request, 'orders/my_books.html', contex)
    else:
        return redirect('login_required')

def CHECKOUT(request, book_id):
    action = request.GET.get('action')
    if request.user.is_authenticated:
        book = Usercart.objects.get(book_id=book_id,user=request.user)
        discount_mrp = int((book.book.price * book.book.discount)/100)
        if request.method == 'POST':
            name = request.POST.get('fname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            amount = (int(book.book.price) - int(discount_mrp)) * 100

            note = {
                'name': name,
                'email': email,
                'phone': phone,
            }
            client = razorpay.Client(auth=(secreate_key, secreate_id))
            receipt = f"Bookseller-{int(time())}"
            order = client.order.create(dict(amount=amount, currency='INR'))

            # Save Payment in DB
            payment = Payment(
                user=request.user,
                book=book.book,
                amount=amount/100,
                order_id=order.get('id'),
            )
            payment.save()

            # Pass order details to the template
            context = {
                'order': order,
                'book': book,
                }
            return render(request, 'checkout/checkout.html', context)
        contex = {
            'book': book,
            'discount_mrp': discount_mrp,
        }
        return render(request, 'checkout/checkout.html', contex)
    else:
        return redirect('login_required')
    


@csrf_exempt
def VERIFY_PAYMENT(request):
    if request.method == "POST":
        data = request.POST
        print("Payment Verification Data:", data)
        try:
            params_dict = {
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature'),
            }
            client = razorpay.Client(auth=(secreate_key, secreate_id))

            # Verify Razorpay signature
            client.utility.verify_payment_signature(params_dict)
            razorpay_order_id = data['razorpay_order_id'],
            razorpay_payment_id = data['razorpay_payment_id'],


            # Fetch the payment record
            payment = Payment.objects.get(order_id=data['razorpay_order_id'])
            payment.payment_id = data['razorpay_payment_id']
            payment.status = True
            userbook = Userbooks(
                user=payment.user,
                book=payment.book,
            )
            userbook.save()
            payment.user_book = userbook
            payment.save()
            usercart = Usercart.objects.get(book=payment.book,user=request.user)
            usercart.delete()

            context = {
                'data': data,
                'payment': payment,
            }
            return render(request, 'verify_payment/success.html',context)
        except:
            return render(request,'verify_payment/fail.html')

def USER_PROFILE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists() and not username==request.user.username:
            messages.warning(request, 'Username already exists')
            return redirect('profile')
        if User.objects.filter(email=email).exists() and not email==request.user.email:
            messages.warning(request, 'email already exists')
            return redirect('profile')
        user = request.user
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.save()
        messages.success(request, 'Profile updated successfuly...!')
        return redirect('profile')
    return render(request, 'registration/profile.html')



def VIEW_BOOK_PAGES(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user.is_authenticated:
        if Userbooks.objects.filter(user=request.user, book=book_id):
            pages = book.pages.all().order_by('page_number')
    else:
        pages = book.pages.all().order_by('page_number')[0:10]
        messages.warning(request, 'You exceed free book reading limit...')
    return render(request, 'details/book_pages.html', {'book': book, 'pages': pages})
