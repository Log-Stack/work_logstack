# Generated by Django 3.1 on 2021-11-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='vacation',
            field=models.FloatField(default=0.0),
        ),
    ]
