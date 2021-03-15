from django import forms
from heartbits_app.models import User


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
