from django.forms import ModelForm, CharField, TextInput, Textarea

from .models import Author, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=100, widget=TextInput(attrs={"class": "form-control"}))
    born_date = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control"}))
    born_location = CharField(max_length=50, widget=TextInput(attrs={"class": "form-control"}))
    bio = CharField(widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'bio']


class QuoteForm(ModelForm):
    author = CharField(max_length=100, widget=TextInput(attrs={"class": "form-control"}))
    quote = CharField(widget=Textarea(attrs={"class": "form-control"}))
    tags = CharField(max_length=100, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Quote
        fields = ['author', 'quote', 'tags']
