# Generated by Django 3.2.6 on 2021-09-09 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20210909_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='creator',
            field=models.EmailField(max_length=254),
        ),
    ]
