# Generated by Django 5.0.6 on 2025-03-29 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_book_book_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='other_name',
        ),
    ]
