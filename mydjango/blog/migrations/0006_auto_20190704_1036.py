# Generated by Django 2.2.1 on 2019-07-04 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190629_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ('-id',)},
        ),
    ]
