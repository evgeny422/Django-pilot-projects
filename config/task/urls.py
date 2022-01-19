from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path("task/", views.TaskViewSet.as_view({'get': 'list'}), name='task-list'),
    path("task/<int:pk>/", views.TaskViewSet.as_view({'get': 'retrieve'})),
    path("task/<int:pk>/delete", views.TaskViewSet.as_view({'get': 'delete'})),

])
