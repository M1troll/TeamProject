from django import forms
from heartbits.heartbits_app.models import User


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=24,
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )
    password2 = forms.CharField(
        max_length=24,
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        help_text=_("Введите такой же пароль для подтверждения."),
    )
    field_order = ['username', 'password', 'password2']

    class Meta:
        model = User
        exclude =['date_register', 'last_online', 'is_blocked', 'coefficient', 'coef_range_max', 'coef_range_min',
                  'test', 'status', 'display_status']