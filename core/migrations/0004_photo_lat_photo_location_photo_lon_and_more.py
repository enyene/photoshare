# Generated by Django 4.1.1 on 2022-09-08 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_viewedphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='location',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='photo',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='ViewedPhoto',
        ),
    ]
