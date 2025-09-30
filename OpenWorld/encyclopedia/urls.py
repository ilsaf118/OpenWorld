from django.urls import path
from .views import index, article, create_article, get_all_actricles, detail, search_articles
from .views import edit_article, delete_article

urlpatterns = [
    path('', index, name='home'),
    path('articles/', article, name='articles'),
    path('create_article/', create_article, name='create_article'),
    path('get_articles/', get_all_actricles, name='get_articles'),
    path('detail/<str:article_id>/', detail, name='article_detail'),
    path('search/', search_articles, name='search_articles'),
    path('article/<str:article_id>/edit/', edit_article, name='edit_article'),
    path('article/<str:article_id>/delete/', delete_article, name='delete_article'),
]