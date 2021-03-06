from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()  # выведет все объекты из модели
    serializer_class = BookSerializer
    # определим фильтрацию
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # права пользователя, только авторизованные могут вносить изменения в БД
    # permission_classes = [IsAuthenticatedOrReadOnly]

    # внесем изменения в права, CRUD могут делать только book.owner
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    filter_fields = ['price']  # http://127.0.0.1:8000/book/?price=1000
    search_fields = ['author_name', 'title']  # http://127.0.0.1:8000/book/?search=Hemingway
    ordering_fields = ['price', 'author_name']  # http://127.0.0.1:8000/book/?ordering=price

    # для присваниявиня owner при создании book
    def perform_create(self, serializer):
        # serializer.validated_data - данные сериализатора после прохождения валидации
        serializer.validated_data[
            'owner'] = self.request.user  # user т.к. create может делать только авторизованный пользователь
        serializer.save()


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    # Поле модели, которое следует использовать для поиска объектов в отдельных экземплярах модели. По умолчанию 'pk'
    lookup_field = 'book'

    def get_object(self):
        # book_id=self.kwargs['book'] приходит с lookup_field
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])  # т.к. лайка может и не быть
        return obj


def auth(request):
    return render(request, 'oauth.html')
