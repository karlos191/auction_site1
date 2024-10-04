# Generated by Django 5.1.1 on 2024-10-04 11:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_comment_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='rating',
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]