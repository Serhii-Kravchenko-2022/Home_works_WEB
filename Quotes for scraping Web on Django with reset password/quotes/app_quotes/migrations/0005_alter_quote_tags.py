# Generated by Django 4.1.6 on 2023-02-09 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_quotes', '0004_remove_quote_tags_delete_tag_quote_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='tags',
            field=models.CharField(max_length=100),
        ),
    ]
