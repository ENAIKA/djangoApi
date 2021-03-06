# Generated by Django 3.0.7 on 2020-06-10 20:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('points', '0003_auto_20200610_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
        migrations.AlterField(
            model_name='rates',
            name='content',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
        migrations.AlterField(
            model_name='rates',
            name='design',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
        migrations.AlterField(
            model_name='rates',
            name='usability',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
