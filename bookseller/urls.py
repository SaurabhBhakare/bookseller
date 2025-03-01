
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
    path('my_cart', views.MY_CART, name='my_cart')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)