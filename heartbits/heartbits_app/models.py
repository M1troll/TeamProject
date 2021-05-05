from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.contrib.auth.models import AbstractUser
from math import sqrt
from operator import itemgetter

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
    user_image = models.ImageField('Изображение', upload_to='user_photos/', blank=True, default='user_photos/default_user.jpg')
    date_joined = models.DateField('Дата регистрации', auto_now_add=True)
    last_login = models.DateTimeField('Заходил последний раз', auto_now_add=True, null=True)
    is_blocked = models.BooleanField('Заблокирован', default=False)
    coefficient = models.FloatField('Коэффициент', default=0.0)
    partner_sex = models.CharField('Пол партнера', choices=SEX, max_length=2, default=SEX[2])
    partner_max_age = models.PositiveSmallIntegerField('Максимальный возраст партнера', default=18)
    user_url = models.SlugField('URL пользователя', max_length=160, unique=True)
    coef_range_min = models.FloatField('Нижняя граница поиска', default=0.0)
    coef_range_max = models.FloatField('Верхняя граница поиска', default=0.0)
    status = models.CharField('Статус', choices=STATUS, max_length=5, null=False)
    display_status = models.BooleanField('Отображение статуса', default=True)

    def get_absolute_url(self):
        return reverse("user_update", kwargs={"slug": self.user_url})

    def calculate_age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    @classmethod
    def __dist_cosin(cls, vec_a, vec_b):
        def dot_product(vec_a, vec_b):
            d = 0.0
            for dim in vec_a:
                if dim in vec_b:
                    d += vec_a[dim] * vec_b[dim]
            return d
        return dot_product(vec_a, vec_b) / sqrt(dot_product(vec_a, vec_a)) / sqrt(dot_product(vec_b, vec_b))

    @classmethod
    def make_recommendation(cls, user_instance):
        tests = Test.objects.all()
        test_results = {test.user.id: test.result for test in tests if test.result is not None}
        matches = [(u, cls.__dist_cosin(test_results[user_instance.id], test_results[u]))
                   for u in test_results
                   if u != user_instance.id and
                   1 - cls.__dist_cosin(test_results[user_instance.id], test_results[u]) <= 0.3]
        best_matches = sorted(matches, key=itemgetter(1), reverse=True)
        return best_matches

    def __str__(self):
        return '%s, %s' % (self.first_name, self.calculate_age())

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Answer(models.Model):
    """Answer Model"""
    question = models.ForeignKey('Question', verbose_name='Вопрос', on_delete=models.CASCADE, null=True)
    answer = models.CharField('Ответ', max_length=500)
    weight = models.FloatField('Вес', default=0.0)

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
    user = models.OneToOneField('User', verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)
    test_title = models.CharField('Название теста', max_length=300)
    test_description = models.TextField('Описание теста', max_length=5000)
    test_questions = models.ManyToManyField(Question, verbose_name='Вопросы', related_name='test_questions')
    result = models.JSONField('Результаты теста', null=True)
    test_url = models.SlugField('URL теста', unique=True)

    def __str__(self):
        return self.test_title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


@receiver(post_save, sender=User)
def create_test(sender, instance, raw=True, **kwargs):
    new_test, created = Test.objects.get_or_create(test_title='Тест на совместимость',
                                                   test_description='Пройдите этот тест и узнайте, с кем вы совместимы!',
                                                   test_url='comp_test_%s' % instance.id,
                                                   user=instance)
    if created:
        new_test.save()
        questions = Question.objects.all()
        for question in questions:
            new_test.test_questions.add(question)
        new_test.save()
    return kwargs
