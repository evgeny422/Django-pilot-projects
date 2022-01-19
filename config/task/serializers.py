from rest_framework import serializers

from .models import *


class TaskListSerializer(serializers.ModelSerializer):
    """Вывод всех задач"""

    class Meta:
        model = Task
        fields = ("url", "user", "category",)


class TaskDetailSerializer(serializers.ModelSerializer):
    """ Описание задачи """

    class Meta:
        model = Task
        fields = '__all__'
