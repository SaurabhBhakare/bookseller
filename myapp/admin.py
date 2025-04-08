from django.contrib import admin
from .models import*
from django.core.exceptions import ValidationError
from django.contrib import messages


class BookPageInline(admin.TabularInline):  # Inline display inside Book
    model = BookPage
    extra = 0  # Don't show extra empty fields
    ordering = ['page_number']  # Sort pages by page number

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category')  # Customize book listing
    # inlines = [BookPageInline]  # Embed pages inside book entry


# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Book,BookAdmin)
admin.site.register(Contact)
admin.site.register(Userbooks)
admin.site.register(Usercart)
admin.site.register(Payment)

admin.site.register(BookPage)