from django.db import models
from django.urls import reverse


class Women(models.Model):
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='URL')
    content = models.TextField(blank=True)
    photo = models.ImageField('Фото', upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Известные люди'
        verbose_name_plural = 'Известные люди'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField('название', max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
