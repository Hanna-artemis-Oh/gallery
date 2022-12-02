# Generated by Django 3.2 on 2022-11-30 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0010_autoartuploadmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='artuploadmodel',
            name='like_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='artuploadmodel',
            name='result_favorite',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='keywordmodel',
            name='word',
            field=models.CharField(blank=True, default='', max_length=255, unique=True),
        ),
    ]
