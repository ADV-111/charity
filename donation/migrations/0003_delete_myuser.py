# Generated by Django 3.0.5 on 2020-05-01 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_auto_20200501_1137'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]