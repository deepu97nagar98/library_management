# Generated by Django 4.2.11 on 2024-05-05 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0002_alter_transaction_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
