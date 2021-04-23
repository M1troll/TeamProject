from datetime import date
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext, gettext
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from heartbits_app.custom_validators import custom_validate_slug, CustomMinValueValidator, CustomMaxValueValidator
from heartbits_app.models import User, Test


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
    )
    partner_max_age = forms.IntegerField(
        label='Максимальный возраст партнера',
        validators=[CustomMinValueValidator(18), CustomMaxValueValidator(99)]
    )
    user_url = forms.CharField(
        max_length=160,
        label='URL пользователя',
        validators=[custom_validate_slug]
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise ValidationError(
                ngettext('Пользователь с таким именем пользователя уже существует.',
                         'Пользователь с таким именем пользователя уже существует.',
                         None),
                code='username_exists',
            )
        return username

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
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'birthday', 'sex',
                  'partner_sex', 'partner_max_age', 'user_country', 'user_city', 'user_description', 'user_image',
                  'user_url']


class MyPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': gettext('Пароли не совпадают.'),
        'password_incorrect': gettext("Ваш текущий пароль введен некорректно. Пожалуйста, введите его снова."),
    }

    old_password = forms.CharField(
        label=gettext("Текущий пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    new_password1 = forms.CharField(
        label=gettext("Новый пароль"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=gettext("Подтвердите новый пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


    # def clean(self):
    #     if check_password(self.cleaned_data['old_password'], self.instance.password):
    #         if self.cleaned_data['password'] == self.cleaned_data['password2']:
    #             self._validate_unique = True
    #             return self.cleaned_data
    #         else:
    #             raise ValidationError(
    #                 gettext('Пароли не совпадают'),
    #                 code='pw_dont_match'
    #             )
    #     else:
    #         raise ValidationError(
    #             gettext('Неверный старый пароль.'),
    #             code='old_pw_wrong'
    #         )
