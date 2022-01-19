from django.contrib import admin

from .models import Task


@admin.register(Task)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("url", "category", "user", "status")
    list_display_links = ("url",)
