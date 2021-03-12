from django.contrib import admin
from .models import UserRating, User, Question, Answer, Test

# Register your models here.

admin.site.register(User)
admin.site.register(UserRating)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Test)
