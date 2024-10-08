# Generated by Django 5.1.1 on 2024-09-29 08:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_is_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watched_auctions', to=settings.AUTH_USER_MODEL),
        ),
    ]
