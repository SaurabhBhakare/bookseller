from django.contrib import admin
from .models import*
from django.core.exceptions import ValidationError
from django.contrib import messages


# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Contact)
admin.site.register(Userbooks)
admin.site.register(Usercart)
admin.site.register(Payment)