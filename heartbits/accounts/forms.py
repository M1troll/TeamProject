from django import forms
from heartbits_app.models import User, Test
from datetime import date
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# class RegisterUserForm(forms.ModelForm):
#     password = forms.CharField(
#         max_length=24,
#         label='Введите пароль',
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
#     )
#     password2 = forms.CharField(
#         max_length=24,
#         label='Подтвердите пароль',
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
#         help_text="Введите такой же пароль для подтверждения.",
#     )
#     field_order = ['username', 'password', 'password2']
#
#     class Meta:
#         model = User
#         exclude = ['date_register', 'last_online', 'is_blocked', 'coefficient', 'coef_range_max', 'coef_range_min',
#                    'test', 'status', 'display_status', 'is_active', 'is_staff', 'is_superuser', 'user_permissions',
#                    'groups']
#         widgets = {
#             'birthday': forms.SelectDateWidget(years=range(date.today().year - 50, date.today().year),
#             attrs={'class': 'form-control'}),
#         }


class LoginUserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=24,
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
            max_length=24,
            label='Введите пароль',
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        )
    password2 = forms.CharField(
            max_length=24,
            label='Подтвердите пароль',
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
            help_text="Введите такой же пароль для подтверждения.",
        )
    # field_order = ['username', 'password', 'password2']

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'birthday', 'sex',
                  'partner_sex', 'partner_max_age', 'user_country', 'user_city', 'user_description', 'user_image',
                  'user_url']
        widgets = {
                    'birthday': forms.SelectDateWidget(years=range(date.today().year - 50, date.today().year),
                                                       attrs={'class': 'form-control'}),
                }


class MyUserChangeForm(UserChangeForm):
    password = forms.CharField(
        max_length=24,
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'}),
    )
    password2 = forms.CharField(
        max_length=24,
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите новый пароль'}),
        help_text="Введите такой же пароль для подтверждения.",
    )
    field_order = ['username', 'password', 'password2']

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'birthday', 'sex',
                  'user_country', 'user_city', 'user_description', 'user_image', 'user_url']
