# Generated by Django 3.1.2 on 2020-12-07 01:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_item_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='likes',
            field=models.ManyToManyField(default=0, related_name='item_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
