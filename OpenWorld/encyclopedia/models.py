from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.CharField('id', max_length=200, primary_key=True)
    image_url = models.URLField('Адрес картинки', max_length=250, null=True)
    title = models.CharField('Название', max_length=150)
    category = models.CharField('Категория', max_length=150)
    tags = models.CharField('Теги', max_length=150)
    content = models.TextField('Контент')
