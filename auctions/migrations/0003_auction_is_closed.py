# Generated by Django 5.1.1 on 2024-09-25 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_user_auction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
