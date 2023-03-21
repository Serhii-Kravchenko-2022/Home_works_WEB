from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.CharField(max_length=100)
    born_location = models.CharField(max_length=100)
    bio = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.fullname}'

    @classmethod
    def create(cls, **kwargs):
        """
        Create class Author object from Autor.json file
        :param kwargs: dict from json
        :return: class Author object
        """
        author = cls.objects.create(
            fullname=kwargs['fullname'],
            born_date=kwargs['born_date'],
            born_location=kwargs['born_location'],
            bio=kwargs['bio']
        )
        return author


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None)
    quote = models.TextField()
    tags = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.author}: {self.quote}'

    @classmethod
    def create(cls, **kwargs):
        """
        Create class Quote object from quotes.json file
        :param kwargs: dict from json
        :return: class Quote object
        """
        quote = cls.objects.create(
            author=Author.objects.filter(fullname=kwargs['author']).get(),
            quote=kwargs['quote'],
            tags=kwargs['tags'],
        )
        return quote
