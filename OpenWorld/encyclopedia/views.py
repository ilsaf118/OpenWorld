from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from .forms import ArticleForm, FileArticleForm
from .models import Article
import os
import json
import uuid


created_articles = {

}

if not os.path.exists('articles/'):
    os.makedirs('articles')

def load():
    for file in os.listdir('articles'):
        with open(f'articles\\{file}', 'r') as f:
            data = json.load(f)
            created_articles.setdefault(data['id'], data)

def add_article(article_data):
    with open(f'articles\\{article_data["id"]}', 'w') as f:        
        json.dump(article_data, f)
    created_articles.setdefault(article_data['id'], article_data)


def check_article(title: str):
    f = 1
    for article in created_articles.values():
        f *= article['title'] != title
        if not f:
            return f
    return (not Article.objects.filter(title=title).exists()) * f

load()


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
    print(created_articles)
    ret_articles = []
    ret_articles.extend(created_articles.values())
    ret_articles.extend(Article.objects.all())
    resp = render(req, 'article.html', {'articles': ret_articles, 'theme': theme})

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
        if 'title' in req.POST:
            form = ArticleForm(req.POST)
            if form.is_valid():
                data = form.cleaned_data
                if 'id' in data.keys():
                    del data['id']
                data['id'] = uuid.uuid4().hex
                if data['export_type'] == 'json':
                    del data['export_type']
                    if check_article(data['title']):
                        add_article(data)
                elif data['export_type'] == 'db':
                    del data['export_type']
                    if check_article(data['title']):
                        Article.objects.create(**data)
            print(Article.objects.all())
        else:
            form  = FileArticleForm(req.POST, req.FILES)
            if form.is_valid():
                file = req.FILES['file']
                content = file.read()
                try:
                    data = json.loads(content)
                except:
                    return "Not true"
                #TODO заменить заглушку
                if 'id' in data:
                    del data['id']
                    data['id'] = uuid.uuid4().hex
                f = 1

                fields = ['title', 'category', 'tags', 'content']
                for field in fields:
                    f *= field in data
                    if not f:
                        break
                print(data)
                if f:
                    print('added')
                    add_article(data)

    return render(req, 'create_article.html', {'theme': theme})


def get_all_actricles(req):
    http_response = HttpResponse(json.dumps(created_articles), content_type='application/json')
    http_response['Content-Disposition'] = f'attachment; filename="all_articles.json"'
    return http_response

def detail(req, article_id: str):
    if article_id in created_articles.keys():
        article = created_articles[article_id]
    elif Article.objects.filter(id=article_id).exists():
        article = Article.objects.get(id=article_id)
    else:
        return HttpResponse('Not found')
    return render(req, 'article_detail.html', {'article': article})


def search_articles(request):
    query = request.GET.get('q', '').strip()
    source_param = request.GET.get('source', 'json,db')  # по умолчанию — оба

    # Определяем, какие источники включены
    sources = source_param.split(',')
    use_json = 'json' in sources
    use_db = 'db' in sources

    results = []

    # Поиск в JSON-статьях
    if use_json:
        for art in created_articles.values():
            if query.lower() in art['title'].lower() or query.lower() in art['content'].lower():
                # Добавим метку источника для отладки (опционально)
                art_with_source = art.copy()
                art_with_source['source'] = 'json'
                results.append(art_with_source)

    # Поиск в БД-статьях
    if use_db:
        db_articles = Article.objects.filter(
            title__icontains=query
        ) | Article.objects.filter(
            content__icontains=query
        )
        for art in db_articles:
            results.append({
                'id': str(art.id),
                'title': art.title,
                'category': art.category,
                'content': art.content,
                'image_url': art.image_url,
                'source': 'db',  # опционально
            })

    return JsonResponse({'articles': results})


def edit_article(request, article_id: str):
    theme = request.COOKIES.get('theme', 'light')

    # Определяем, откуда статья: из JSON или из БД
    is_json = article_id in created_articles
    is_db = Article.objects.filter(id=article_id).exists()

    if not (is_json or is_db):
        return HttpResponse('Статья не найдена', status=404)

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Убираем export_type и id из данных
            if 'export_type' in data:
                del data['export_type']
            data['id'] = article_id  # сохраняем тот же ID!

            if is_json:
                # Обновляем JSON-файл
                old_path = f'articles/{article_id}'
                if os.path.exists(old_path):
                    os.remove(old_path)
                add_article(data)
                created_articles[article_id] = data
            elif is_db:
                # Обновляем в БД
                Article.objects.filter(id=article_id).update(**data)

            return redirect('article_detail', article_id=article_id)
    else:
        # Заполняем форму начальными данными
        if is_json:
            initial_data = created_articles[article_id]
        else:
            art = Article.objects.get(id=article_id)
            initial_data = {
                'title': art.title,
                'category': art.category,
                'content': art.content,
                'image_url': art.image_url,
                'export_type': 'db',  # чтобы форма знала, куда сохранять
            }
        form = ArticleForm(initial=initial_data)

    return render(request, 'article_edit.html', {
        'form': form,
        'theme': theme,
        'article_id': article_id,
        'is_json': is_json,
        'is_db': is_db,
    })



def delete_article(request, article_id: str):
    if request.method != "POST":
        return HttpResponse("Метод не разрешён", status=405)

    # Удаляем из JSON
    if article_id in created_articles:
        file_path = f'articles/{article_id}'
        if os.path.exists(file_path):
            os.remove(file_path)
        del created_articles[article_id]

    # Удаляем из БД
    Article.objects.filter(id=article_id).delete()

    return redirect('articles')  # перенаправляем на список статей