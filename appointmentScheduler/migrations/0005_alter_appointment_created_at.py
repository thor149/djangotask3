# Generated by Django 5.0.7 on 2024-08-01 17:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "appointmentScheduler",
            "0004_remove_doctor_profile_remove_doctor_specialty_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 8, 1, 17, 37, 51, 529755, tzinfo=datetime.timezone.utc
                ),
                editable=False,
            ),
        ),
    ]
