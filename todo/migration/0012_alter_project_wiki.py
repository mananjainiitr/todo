# Generated by Django 3.2.6 on 2021-09-04 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0011_auto_20210904_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='wiki',
            field=models.TextField(),
        ),
    ]
