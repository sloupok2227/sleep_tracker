# Generated by Django 5.1.4 on 2024-12-16 15:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleep', '0010_sleeprecord_visibility_alter_sleeprecord_profile_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_requests_sent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_requests_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sleeprecord',
            name='visibility',
            field=models.CharField(choices=[('private', 'Только я'), ('friends', 'Друзья'), ('public', 'Все')], default='private', max_length=10),
        ),
    ]
