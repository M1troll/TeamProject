from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.

SEX = [
    ('M', 'Man'),
    ('W', 'Woman'),
    ('ND', 'Not defined')
]

STATUS = [
    ('ON', 'Online'),
    ('OFF', 'Offline'),
    ('G', 'Gone'),
    ('S', 'Sleep')
]


class UserRating(models.Model):
    """User Rating Model"""
    user = models.ForeignKey('User', verbose_name='Пользователь', related_name='user',
                                on_delete=models.CASCADE, default=-1)
    id_user_liked = models.ForeignKey('User', verbose_name='Кто поставил', related_name='user_liked',
                                      on_delete=models.CASCADE, default=-1)

    # def __str__(self):
    #     return '%s' % self.count_likes()

    class Meta:
        unique_together = ('user', 'id_user_liked')
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class User(AbstractUser):
    """User Model"""
    username = models.CharField('Имя пользователя', max_length=50, unique=True)
    password = models.CharField('Пароль', max_length=100)
    email = models.EmailField('E-mail')
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    birthday = models.DateField('День рождения', default=date.today)
    sex = models.CharField('Пол', choices=SEX, max_length=2, default=SEX[2])
    user_country = models.CharField('Страна', max_length=100)
    user_city = models.CharField('Город', max_length=100)
    user_description = models.TextField('Описание', max_length=5000)
    user_image = models.ImageField('Изображение', upload_to='user_photos/', blank=True)
    date_joined = models.DateField('Дата регистрации', auto_now_add=True)
    last_login = models.DateTimeField('Заходил последний раз', auto_now_add=True, null=True)
    is_blocked = models.BooleanField('Заблокирован', default=False)
    coefficient = models.FloatField('Коэффициент', default=0.0)
    user_url = models.SlugField('URL пользователя', max_length=160, unique=True)
    test = models.OneToOneField('Test', verbose_name='Тест', on_delete=models.SET_NULL, null=True, blank=True)
    coef_range_min = models.FloatField('Нижняя граница поиска', default=0.0)
    coef_range_max = models.FloatField('Верхняя граница поиска', default=0.0)
    status = models.CharField('Статус', choices=STATUS, max_length=5, null=False)
    display_status = models.BooleanField('Отображение статуса', default=True)

    def calculate_age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def __str__(self):
        return '%s, %s' % (self.first_name, self.calculate_age())

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Answer(models.Model):
    """Answer Model"""
    question = models.ForeignKey('Question', verbose_name='Вопрос', on_delete=models.CASCADE, null=True)
    answer = models.CharField('Ответ', max_length=500)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'


class Question(models.Model):
    """Question Model"""
    title = models.CharField('Заголовок вопроса', max_length=300)
    description = models.TextField('Описание вопроса', max_length=5000)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Test(models.Model):
    """Test Model"""
    test_title = models.CharField('Название теста', max_length=300)
    test_description = models.TextField('Описание теста', max_length=5000)
    test_questions = models.ManyToManyField(Question, verbose_name='Вопросы', related_name='test_questions')
    test_result = models.CharField('Результаты теста', max_length=500, blank=True)
    test_url = models.SlugField('URL теста', unique=True)

    def __str__(self):
        return self.test_title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
