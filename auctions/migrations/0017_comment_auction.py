# Generated by Django 5.1.1 on 2024-10-08 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_comment_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auction'),
        ),
    ]