# Generated by Django 4.2.11 on 2024-05-05 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0003_alter_book_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=1000),
        ),
    ]
