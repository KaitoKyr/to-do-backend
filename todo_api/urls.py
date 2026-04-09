
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import tasksView, tasksViewDetailed, tagsView, tagDetailView

urlpatterns = [
    path("todos/", tasksView, name='todos'),
    path('todos/<int:pk>/', tasksViewDetailed, name='task_detail'),
    path("tags/", tagsView, name='tags'),
    path("tags/<int:pk>/", tagDetailView)
]