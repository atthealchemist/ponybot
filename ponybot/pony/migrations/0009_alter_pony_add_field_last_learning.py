# Generated by Django 3.2.5 on 2021-07-10 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pony', '0008_alter_pony_add_is_alive_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='pony',
            name='last_learning',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
