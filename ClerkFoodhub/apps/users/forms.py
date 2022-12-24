from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'password')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'departament',
            'first_name', 'last_name',
            'email', 'phone',
            'ordering',
            'last_login', 'date_joined',
            'is_active', 'is_staff', 'is_superuser',
            'user_permissions', 'groups'
        )