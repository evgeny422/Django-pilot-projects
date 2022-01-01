from rest_framework.serializers import ModelSerializer

# сериализатор для работы с моделью во view
from store.models import Book


class BookSerializer(ModelSerializer):  # определяем из каких полей сформируется json
    class Meta:
        model = Book
        fields = '__all__'
