# Generated by Django 2.2.1 on 2019-06-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_person_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='date',
        ),
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.CharField(default='神秘人', max_length=20),
        ),
    ]