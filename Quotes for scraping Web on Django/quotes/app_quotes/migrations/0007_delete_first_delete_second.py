# Generated by Django 4.1.6 on 2023-02-09 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_quotes', '0006_first_second'),
    ]

    operations = [
        migrations.DeleteModel(
            name='First',
        ),
        migrations.DeleteModel(
            name='Second',
        ),
    ]
