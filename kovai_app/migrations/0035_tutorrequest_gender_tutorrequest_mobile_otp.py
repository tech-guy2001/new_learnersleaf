# Generated by Django 4.1.1 on 2024-12-06 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kovai_app', '0034_remove_tutorregistration_online_experience_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorrequest',
            name='gender',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='mobile_otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
