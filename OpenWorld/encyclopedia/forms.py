from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=250)
    category = forms.CharField(max_length=250)
    tags = forms.CharField()
    content = forms.CharField()
    