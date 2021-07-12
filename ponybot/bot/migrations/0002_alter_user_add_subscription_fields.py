# Generated by Django 3.2.5 on 2021-07-12 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ponybotuser',
            name='is_subscriber',
            field=models.BooleanField(default=False, verbose_name='Is Subscriber'),
        ),
        migrations.AddField(
            model_name='ponybotuser',
            name='subscribed_at',
            field=models.DateTimeField(null=True, verbose_name='Subscribed At'),
        ),
    ]