from django import forms


class ArticleForm(forms.Form):
    image_url = forms.URLField(max_length=250, label='URL картинки')
    title = forms.CharField(max_length=250, label='Название')
    category = forms.CharField(max_length=250, label='Категории')
    export_type = forms.CharField(max_length=5)
    tags = forms.CharField(max_length=150, label='Теги')
    content = forms.CharField(label='Контент')


class FileArticleForm(forms.Form):
    file = forms.FileField()


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=150)
    result_type = forms.CharField(max_length=50)