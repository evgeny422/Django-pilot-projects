from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField('title', max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)  # 7 знаков, максимально 2 знака после запятой
    author_name = models.CharField(max_length=255, blank=True)
    # related_name='имя связи' позволяет избавиться от конфликта, когда от юзера к бук идет 2 связи, тем самым
    # стандартные related_name у owner и readers имеют одно и то же название => делаем их уникальными
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')
    # => User.objects.get(pk=1).my_books.all() где my_books - заданное related_name

    def __str__(self):
        return f'{self.id} :  {self.title}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )

    # отношения юзер - книга
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField('В закладке', default=False)
    rate = models.PositiveSmallIntegerField('Оценка', choices=RATE_CHOICES, null=True)  # прописываем варианты выбора

    def __str__(self):
        return f'{self.user.username} , {self.book.title} ,RATING: {self.rate}'
