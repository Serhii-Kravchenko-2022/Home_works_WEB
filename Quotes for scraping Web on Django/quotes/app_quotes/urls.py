from django.urls import path

from . import views

app_name = 'app_quotes'

urlpatterns = [
    path('', views.main, name='main'),
    path('author/<str:author_name>', views.author, name='author'),
    path('tag/<str:tag>', views.tag, name='tag'),
    path('add_author', views.add_author, name='add_author'),
    path('add_quote', views.add_quote, name='add_quote')
]
