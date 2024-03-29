# Generated by Django 4.2.1 on 2023-08-08 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_photocontestsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='dislikes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='photocontestsubmission',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
