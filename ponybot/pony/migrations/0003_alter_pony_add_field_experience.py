# Generated by Django 3.2.5 on 2021-07-05 13:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pony', '0002_alter_pony_add_field_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pony',
            name='experience',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Pony experience'),
        ),
    ]
