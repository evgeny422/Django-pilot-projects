from rest_framework.serializers import ModelSerializer

# сериализатор для работы с моделью во view
from store.models import *


class BookSerializer(ModelSerializer):  # определяем из каких полей сформируется json
    class Meta:
        model = Book
        fields = '__all__'


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
