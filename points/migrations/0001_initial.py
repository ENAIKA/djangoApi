# Generated by Django 3.0.7 on 2020-06-07 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('bio', models.TextField()),
                ('projects', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
            ],
        ),
    ]
