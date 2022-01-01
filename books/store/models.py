from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField('title', max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)  # 7 знаков, максимально 2 знака после запятой
    author_name = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id} :  {self.title}'
