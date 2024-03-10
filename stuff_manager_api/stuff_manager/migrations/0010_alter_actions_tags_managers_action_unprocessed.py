# Generated by Django 5.0.1 on 2024-03-06 23:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stuff_manager", "0009_action_energy"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="actions_tags",
            managers=[],
        ),
        migrations.AddField(
            model_name="action",
            name="unprocessed",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stuff_manager.unprocessed",
            ),
        ),
    ]