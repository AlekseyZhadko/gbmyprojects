from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Recipe
from .models import CategoryRecipe

''' Форма для работы с рецептами '''


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None

    class Meta:
        description = forms.CharField(widget=CKEditorWidget())
        model = Recipe
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'cooking_steps': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'cooking_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', }),
        }


''' Форма для регистрации пользователя '''


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password1',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Password2',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


''' Форма для авторизации пользователя'''


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'password')
