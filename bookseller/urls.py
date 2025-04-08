from django.contrib import admin
from django.urls import path, include
from myapp import user_login
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HOME, name="home"),
    path('book/<slug:slug>', views.BOOK_DETAILS, name='book_details'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', user_login.REGISTER, name='register'),
    path('dologin/', user_login.DOLOGIN, name='dologin'),
    path('dologout/', user_login.DOLOGOUT, name='dologout'),
    path('author_details/<slug:slug>', views.AUTHOR_DETAILS, name='author_details'),
    path('contact_us/', views.CONTACT_US, name='contact_us'),
    path('about_us/', views.ABOUT_US, name='about_us'),
    path('add_cart/<slug:slug>', views.ADD_CART, name='add_cart'),
    path('remove_cart/<int:book_id>', views.REMOVE_CART, name='remove_cart'),
    path('my_cart/', views.MY_CART, name='my_cart'),
    path('my_books/', views.MY_BOOKS, name='my_books'),
    path('login_required/', views.LOGIN_REQUIRED, name='login_required'),
    path('checkout/<int:book_id>', views.CHECKOUT, name='checkout'),
    path('verify_payment/', views.VERIFY_PAYMENT, name='verify_payment'),
    path('profile/', views.USER_PROFILE, name='profile'),
    path('view_pages/<int:book_id>/', views.VIEW_BOOK_PAGES, name='view_book_pages'),

    # path for cart
    path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),

    path("verify-email/<uidb64>/<token>/",user_login.verify_email, name="verify-email"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)