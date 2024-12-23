# Generated by Django 5.1.4 on 2024-12-15 12:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleep', '0008_alter_physicalactivity_duration_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicalactivity',
            name='calories_burned',
        ),
        migrations.AlterField(
            model_name='diethabit',
            name='food',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='physicalactivity',
            name='activity_type',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='physicalactivity',
            name='duration',
            field=models.DurationField(),
        ),
        migrations.AlterField(
            model_name='sleeprecord',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sleep_records', to='sleep.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
