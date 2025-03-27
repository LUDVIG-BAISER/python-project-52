from django.urls import path
from .views import ListTasks, CreateTask, UpdateTask, DeleteTask, ViewTask


urlpatterns = [
    path('', ListTasks.as_view(), name='home_tasks'),
    path('<int:pk>/', ViewTask.as_view(), name='view_task'),
    path('create/', CreateTask.as_view(), name='create_task'),
    path('<int:pk>/update/', UpdateTask.as_view(), name='update_task'),
    path('<int:pk>/delete/', DeleteTask.as_view(), name='delete_task'),
]
