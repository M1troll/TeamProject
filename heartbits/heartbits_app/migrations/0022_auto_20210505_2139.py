# Generated by Django 3.1.7 on 2021-05-05 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heartbits_app', '0021_auto_20210326_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(blank=True, default='user_photos/default_user.jpg', upload_to='user_photos/', verbose_name='Изображение'),
        ),
    ]
