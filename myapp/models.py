from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class Author(models.Model):
    author_profile = models.ImageField(upload_to='media/author/', max_length = 100)
    author_name = models.CharField(max_length = 150)
    about = models.TextField()
    slug = models.SlugField(default='', max_length = 50, null=True, blank=True)
    
    def __str__(self):
        return self.author_name
    def author(self):
        return Author.objects.all().order_by('id')
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("author_details", kwargs={'slug': self.slug})
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class Category(models.Model):
    category = models.CharField(max_length = 150)
    
    def __str__(self):
        return self.category
    

class Language(models.Model):
    language = models.CharField(max_length = 50)

    def __str__(self):
        return self.language    

class Book(models.Model):
    title = models.CharField(max_length = 50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    discount = models.FloatField()
    short_desc = models.TextField()
    publisher = models.CharField(max_length = 50)
    edition = models.CharField(max_length = 150)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    isbn = models.CharField(max_length = 150)
    year = models.CharField(max_length = 6)
    image = models.ImageField(upload_to='media/covers/', null=True)
    book_file = models.FileField(upload_to='media/book_file/',null=True, blank=True)
    slug = models.SlugField(default='', max_length = 50, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def book(self):
        return Book.objects.all().order_by('id')
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("book_details", kwargs={'slug': self.slug})

class Usercart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + "-" + self.book.title
    
    def get_total_price(self):
        if self.book.discount is None or self.book.discount is 0:
            return self.book.price
        # price = float(price)
        # discount = float(discount)
        sellprice = self.book.price
        sellprice = self.book.price - (self.book.price * self.book.discount/100)
        return int(sellprice)
    
class Userbooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + "-" + self.book.title
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user_book = models.ForeignKey(Userbooks, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(null=True)
    order_id = models.CharField(max_length = 250, unique=True,null=True)
    payment_id = models.CharField(max_length = 250, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name + "-" + self.book.title
    




# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Book.objects.filter(slug=slug).order_by('-id')
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug


# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)


# pre_save.connect(pre_save_post_receiver, Book)


@receiver(pre_save, sender=Author)
def create_author_slug(sender, instance, **kwargs):
    if not instance.slug: 
        instance.slug = slugify(instance.author_name)

@receiver(pre_save, sender=Book)
def create_book_slug(sender, instance, **kwargs):
    if not instance.slug:  
        instance.slug = slugify(instance.title)

class Contact(models.Model):
    name = models.CharField(max_length = 150)
    company = models.CharField(max_length = 150)
    email = models.CharField(max_length = 150)
    mobile = models.CharField(max_length = 150)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    

class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    page_number = models.PositiveIntegerField()
    image = models.ImageField(upload_to='media/book_pages/')

    def __str__(self):
        return f"{self.book.title} - Page {self.page_number}"

