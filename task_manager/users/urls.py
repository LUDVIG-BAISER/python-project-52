from django.urls import path
from .views import ListUsers, SignUp, UpdateUser, DeleteUser


urlpatterns = [
    path('', ListUsers.as_view(), name='home_users'),
    path('create/', SignUp.as_view(), name='create_user'),
    path('<int:pk>/update/', UpdateUser.as_view(), name='update_user'),
    path('<int:pk>/delete/', DeleteUser.as_view(), name='delete_user'),
]
