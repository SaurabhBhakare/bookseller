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
    slug = models.SlugField(default='', max_length = 50, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def book(self):
        return Book.objects.all().order_by('id')
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("book_details", kwargs={'slug': self.slug})
    
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