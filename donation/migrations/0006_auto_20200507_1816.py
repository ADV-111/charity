# Generated by Django 3.0.5 on 2020-05-07 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0005_donation_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='status',
        ),
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
