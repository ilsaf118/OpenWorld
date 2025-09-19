from django.shortcuts import render
from .forms import ArticleForm


created_articles = [

]


# Create your views here.
def index(req):
    theme = req.COOKIES.get('theme', 'light')

    resp = render(req, 'index.html', {'theme': theme})

    if 'theme' not in req.COOKIES:
        resp.set_cookie(
            'theme',
            'light',
            max_age=365 * 24 * 60 * 60,  # 1 год
            samesite='Lax'
        )
    return resp

def article(req):
    theme = req.COOKIES.get('theme', 'light')

    resp = render(req, 'article.html', {'articles': created_articles, 'theme': theme})

    if 'theme' not in req.COOKIES:
        resp.set_cookie(
            'theme',
            'light',
            max_age=365 * 24 * 60 * 60,  # 1 год
            samesite='Lax'
        )
    return resp

def create_article(req):
    theme = req.COOKIES.get('theme', 'light')

    resp = render(req, 'index.html', {'theme': theme})

    if 'theme' not in req.COOKIES:
        resp.set_cookie(
            'theme',
            'light',
            max_age=365 * 24 * 60 * 60,  # 1 год
            samesite='Lax'
        )

    if req.method == "POST":
        form = ArticleForm(req.POST)
        if form.is_valid():
            created_articles.append(form.cleaned_data)
    return render(req, 'create_article.html', {'theme': theme})