# Generated by Django 3.2.6 on 2021-09-06 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0025_auto_20210905_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.EmailField(default='admin@gmail.com', max_length=254),
        ),
    ]
