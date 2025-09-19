from django.urls import path
from .views import index, article, create_article

urlpatterns = [
    path('', index, name='home'),
    path('/articles', article, name='articles'),
    path('/create_article', create_article, name='create_article')
]