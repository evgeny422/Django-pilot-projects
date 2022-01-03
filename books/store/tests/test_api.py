import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


# по факту сравниваем сериализатор с самим собой
class BookApiTestCase(APITestCase):

    def setUp(self):  # запускается перед тестом
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(title='Test book 1', price=25.99, author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(title='Test book 2', price=25.99, author_name='Author 5')
        self.book_3 = Book.objects.create(title='Test book Author 1', price=55, author_name='Author 2')

    def test_get(self):
        # https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        url = reverse('book-list')  # url по которому сделаем запрос; префикс list для получения всех данных
        print(url)  # /book/
        response = self.client.get(url)
        print(response, 'data is  ', response.data)  # вывод запроса, вывод переданных данных через get запрос
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3],
                                         many=True).data  # передаем список объектов для сериализации
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # проверяем код возврата сервера
        self.assertEqual(serializer_data, response.data)  # сравниваем полученные данные

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 55})
        serializer_data = BookSerializer(self.book_3).data
        print(serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})  # выделяем по чему ведется поиск
        serializer_data = BookSerializer([self.book_1, self.book_3], many=True).data
        print('serializer_data', serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # проверяем код возврата сервера
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'author_name'})
        serializer_data = BookSerializer([self.book_1, self.book_3,
                                          self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')

        # данные которые хотим занести в БД
        data = {
            'title': 'Python 3 for developers',
            'price': 350,
            'author_name': 'Dronov',
        }
        # преобразуем данные в json
        json_data = json.dumps(data)
        self.client.force_login(self.user)  # авторизуем юзера для post запроса
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)  # проверка на владельца записи

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))  # args=(self.book_1.id), т.к. обновляем определенную книгу

        # данные которые хотим занести в БД
        data = {
            'title': self.book_1.title,
            'price': 575,
            'author_name': self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()  # необходимо переобределить книгу, т.к. данные цены обновляются в тестовой дб
        self.assertEqual(575, self.book_1.price)

        def test_update(self):
            url = reverse('book-detail',
                          args=(self.book_1.id,))  # args=(self.book_1.id), т.к. обновляем определенную книгу

            # данные которые хотим занести в БД
            data = {
                'title': self.book_1.title,
                'price': 575,
                'author_name': self.book_1.author_name,
            }
            json_data = json.dumps(data)
            self.client.force_login(self.user)
            response = self.client.put(url, data=json_data, content_type='application/json')
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.book_1.refresh_from_db()  # необходимо переобределить книгу, т.к. данные цены обновляются в тестовой дб
            self.assertEqual(575, self.book_1.price)

    def test_update_not_owner(self):  # для безопасности нужно проверять негативные сценарии
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('book-detail', args=(self.book_1.id,))

        data = {
            'title': self.book_1.title,
            'price': 575,
            'author_name': self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual('25.99', f'{self.book_1.price}')

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))

        data = {
            'title': self.book_1.title,
            'price': 575,
            'author_name': self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)


class BooksRelationTestCase(APITestCase):

    def setUp(self):  # запускается перед тестом
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.book_1 = Book.objects.create(title='Test book 1', price=25.99, author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(title='Test book 2', price=25.99, author_name='Author 5')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))  # reverse from home page

        data = {
            'like': True,
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        # update data, method patch не для всех полей, put - передаем все поля для обновления
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # проверяем код возврата сервера
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)  # cause of many to many
        self.assertTrue(relation.like)  # появился ли лайк

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))  # reverse from home page

        data = {
            'rate': 3,
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # проверяем код возврата сервера
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(3, relation.rate)

    def test_in_bookmarks(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))  # reverse from home page

        data = {
            'in_bookmarks': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(True, relation.in_bookmarks)  #
