# Generated by Django 3.2.5 on 2021-07-29 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pony',
            name='gender',
            field=models.CharField(choices=[('Жеребец', 'Stallion'), ('Кобылка', 'Mare')], default='Жеребец', max_length=10, verbose_name='Gender'),
        ),
    ]