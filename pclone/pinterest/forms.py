from django import forms
from django.forms import ModelForm
from .models import Pictures, Pintags, Users
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


# class RegisterUserForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2',)


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2']


class SavePinForm(ModelForm):
    class Meta:
        model = Pictures
        fields = ('pic',)
        labels = {
            'pic': '',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.regtime:  # Only set if not already set
            instance.regtime = timezone.now()
        if commit:
            instance.save()
        return instance

