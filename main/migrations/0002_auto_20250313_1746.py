# Generated by Django 3.0.5 on 2025-03-13 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Информация', 'Информация'), ('DIY', 'DIY')], max_length=15),
        ),
    ]
