from django.db import models
from datetime import date

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
    like = models.PositiveIntegerField('Лайки')
    value = models.PositiveIntegerField('Рейтинг')

    def __str__(self):
        return '%s, %s' % (self.like, self.value)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class User(models.Model):
    username = models.CharField('Имя пользователя', max_length=50)
    password = models.CharField('Пароль', max_length=100)
    email = models.EmailField('E-mail')
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    age = models.PositiveSmallIntegerField('Возраст')
    sex = models.CharField('Пол', choices=SEX, max_length=2, default=SEX[2])
    user_country = models.CharField('Страна', max_length=100)
    user_city = models.CharField('Город', max_length=100)
    user_description = models.TextField('Описание', max_length=5000)
    user_image = models.ImageField('Изображение', upload_to='user_photos/')
    date_register = models.DateField('Дата регистрации', default=date.today)
    last_online = models.DateTimeField('Заходил последний раз')
    is_blocked = models.BooleanField('Заблокирован', default=False)
    rating = models.OneToOneField(UserRating, on_delete=models.SET_NULL, null=True)
    coefficient = models.FloatField('Коэффициент')
    user_url = models.SlugField(max_length=160, unique=True)
    coef_range_min = models.FloatField('Нижняя граница поиска')
    coef_range_max = models.FloatField('Верхняя граница поиска')
    status = models.CharField('Статус', choices=STATUS, max_length=5, null=False)
    display_status = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.first_name, self.age)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Answer(models.Model):
    answer = models.CharField(max_length=500)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'



class Question(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=5000)
    answers = models.ForeignKey(Answer, verbose_name='Ответы', on_delete=models.CASCADE, default=None, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Test(models.Model):
    test_title = models.CharField('Название теста', max_length=300)
    test_description = models.TextField('Описание теста', max_length=5000)
    test_questions = models.ManyToManyField(Question, verbose_name='Вопросы', related_name='test_questions')
    test_result = models.CharField(max_length=500)
    test_url = models.SlugField(unique=True)

    def __str__(self):
        return self.test_title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
