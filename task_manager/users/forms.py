from django.contrib.auth.forms import UserCreationForm
from .models import Users


class UsersForm(UserCreationForm):
    class Meta:
        model = Users
        fields = [
            'first_name',
            'last_name',
            'username',
        ]
