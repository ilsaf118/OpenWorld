from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.CharField('id', max_length=200, primary_key=True)
    image_url = models.URLField('Адрес картинки')
    title = models.CharField('Название')
    category = models.CharField('Категория')
    tags = models.CharField('Теги')
    content = models.TextField('Контент')