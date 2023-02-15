import json
from collections import Counter

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
# from django.core.serializers import serialize
# from django.core.serializers.json import DjangoJSONEncoder
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote


# class LazyEncoderAuthors(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Author):
#             return str(obj)
#         return super().default(obj)
#
#
# class LazyEncoderQuotes(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Quote):
#             return str(obj)
#         return super().default(obj)


# quotes/app_quotes/quotes_data/authors.json

def main(request):
    # if not Author.objects.all():
    #     serialize('app_quotes/quotes_data/authors.json', First.objects.all())
    # if not Quote.objects.all():
    #     serialize('app_quotes/quotes_data/quotes.json', Second.objects.all())

    # seed database from json files
    if not Author.objects.all():
        with open('app_quotes/quotes_data/authors.json', encoding='utf-8') as file:
            json_data = json.loads(file.read())
            for data in json_data:
                Author.create(**data)

    if not Quote.objects.all():
        with open('app_quotes/quotes_data/quotes.json', encoding='utf-8') as file:
            json_data = json.loads(file.read())
            for data in json_data:
                Quote.create(**data)

    quote_items = Quote.objects.all()

    # Top 10 tags

    tag_list = []
    for quote in quote_items:
        tag_list += quote.tags.replace('[', '').replace(']', '').replace("'", '').split(',')
    quote_dict = dict(Counter(tag_list))
    top_data = sorted(quote_dict.items(), key=lambda x: -x[1])[:10]
    top_list = [name[0] for name in top_data]
    # pagination
    p = Paginator(quote_items, 5)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    # context
    context = {'title': 'Killer Instagram',
               'items': page,
               'top': top_list
               }

    return render(request, "app_quotes/index.html", context=context)


def author(request, author_name):
    author_object = Author.objects.filter(fullname=author_name).get()
    return render(request, "app_quotes/author.html", context={'title': 'Quotes',
                                                              'author': author_object})


def tag(request, tag):
    quote_list = [quote for quote in Quote.objects.all() if tag in
                  quote.tags.replace('[', '').replace(']', '').replace("'", '').split(',')]

    return render(request, "app_quotes/tag.html", context={'title': 'Quotes',
                                                           'quotes': quote_list,
                                                           'tag': tag})


def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            auth = form.save(commit=False)
            auth.user = request.user
            auth.save()
            return redirect(to='app_quotes:main')
    return render(request, "app_quotes/add_author.html", context={'title': 'Quotes', 'form': form})


def add_quote(request):
    form = QuoteForm(instance=Quote())
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            quo = form.save(commit=False)
            quo.user = request.user
            quo.save()
            return redirect(to='app_quotes:main')
    return render(request, "app_quotes/add_quote.html", context={'title': 'Quotes', 'form': form})
