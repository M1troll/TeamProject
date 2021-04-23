from difflib import SequenceMatcher
import re
from django.contrib.auth.password_validation import MinimumLengthValidator, UserAttributeSimilarityValidator, \
    CommonPasswordValidator, NumericPasswordValidator
from django.core.validators import RegexValidator, slug_re, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.utils.translation import gettext_lazy, ngettext


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    'Пароль слишком короткий. Минимальное количество символов - %(min_length)d ',
                    'Пароль слишком короткий. Минимальное количество символов - %(min_length)d ',
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length}
            )

    def get_help_text(self):
        return ngettext(
            'Пароль не может быть короче %(min_length)d символов.',
            'Пароль не может быть короче %(min_length)d символов.',
            self.min_length
        ) % {'min_length': self.min_length}


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        ngettext("Пароль слишком похож на %(verbose_name)s.",
                                 "Пароль слишком похож на %(verbose_name)s.",
                                 verbose_name),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return ngettext('Ваш пароль не может быть похож на другую личную информацию.',
                        'Ваш пароль не может быть похож на другую личную информацию.',
                        None)


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                ngettext("Ваш пароль слишком простой.",
                         "Ваш пароль слишком простой.",
                         None),
                code='password_too_common',
            )

    def get_help_text(self):
        return ngettext('Ваш пароль не может быть слишком очевидным.',
                        'Ваш пароль не может быть слишком очевидным.',
                        None)


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                ngettext("Ваш пароль полностью состоит из цифр.",
                         "Ваш пароль полностью состоит из цифр.",
                         None),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return ngettext("Ваш пароль не может полностью состоять из цифр",
                        "Ваш пароль не может полностью состоять из цифр",
                         None)


class CustomMinValueValidator(MinValueValidator):
    message = gettext_lazy('Убедитесь, что заданное значение не меньше %(limit_value)s.')


class CustomMaxValueValidator(MaxValueValidator):
    message = gettext_lazy('Убедитесь, что заданное значение не больше %(limit_value)s.')


custom_validate_slug = RegexValidator(
    slug_re,
    ngettext('Введите валидный URL, cсостоящий из английских букв, цифр, нижних пожчеркиваний или дефисов.',
             'Введите валидный URL, cсостоящий из английских букв, цифр, нижних пожчеркиваний или дефисов.',
             None),
    'invalid'
)

