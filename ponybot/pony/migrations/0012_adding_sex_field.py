# Generated by Django 3.2.5 on 2021-07-10 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pony', '0011_adding_owner_and_conversation_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='pony',
            name='sex',
            field=models.CharField(choices=[('Земнопони', 'Earthpony'), ('Пегас', 'Pegasus'), ('Единорог', 'Unicorn'), ('Аликорн', 'Alicorn')], default='Земнопони', max_length=12, verbose_name='Pony sex'),
        ),
    ]
