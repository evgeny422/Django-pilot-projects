from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(title='Test book 1', price=25.99, author_name='Test1')
        book_2 = Book.objects.create(title='Test book 2', price=25.99, author_name='Test2')
        data = BookSerializer([book_1, book_2], many=True).data
        excpected_data = [  # ожидаемые данные из сериализатора
            {
                'id': book_1.id,
                'title': 'Test book 1',
                'price': '25.99',  # строка т.к. тип данные decimal
                'author_name': 'Test1',
            },

            {
                'id': book_2.id,
                'title': 'Test book 2',
                'price': '25.99',
                'author_name': 'Test2'
            }
        ]
        self.assertEqual(excpected_data, data)
