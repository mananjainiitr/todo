# Generated by Django 3.2.6 on 2021-09-02 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20210902_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regestereduser',
            name='roles',
        ),
        migrations.AddField(
            model_name='regestereduser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='regestereduser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='regestereduser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
