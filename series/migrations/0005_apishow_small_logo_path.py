# Generated by Django 2.1.2 on 2018-10-26 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0004_apishow_first_followed'),
    ]

    operations = [
        migrations.AddField(
            model_name='apishow',
            name='small_logo_path',
            field=models.TextField(help_text='the url leading to small logo path', null=True),
        ),
    ]
