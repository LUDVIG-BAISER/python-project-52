from django.urls import path
from .views import ListStatuses, CreateStatus, UpdateStatus, DeleteStatus

urlpatterns = [
    path('', ListStatuses.as_view(), name='home_statuses'),
    path('create/', CreateStatus.as_view(), name='create_status'),
    path('<int:pk>/update/', UpdateStatus.as_view(), name='update_status'),
    path('<int:pk>/delete/', DeleteStatus.as_view(), name='delete_status')
]
