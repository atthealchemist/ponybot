# Generated by Django 3.2.5 on 2021-07-13 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_alter_user_add_meta'),
    ]

    operations = [
        migrations.CreateModel(
            name='PonybotAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Action Name')),
                ('aliases', models.JSONField(default=list, verbose_name='Action aliases')),
                ('is_admin_only', models.BooleanField(default=False, verbose_name='Is admin only')),
            ],
            options={
                'verbose_name': 'Ponybot Action',
                'verbose_name_plural': 'Ponybot Actions',
            },
        ),
    ]
