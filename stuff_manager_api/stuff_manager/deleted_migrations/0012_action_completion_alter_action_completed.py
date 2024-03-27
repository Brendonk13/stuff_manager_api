# Generated by Django 5.0.1 on 2024-03-27 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stuff_manager", "0011_actioncompletion_action_completed"),
    ]

    operations = [
        migrations.AddField(
            model_name="action",
            name="completion",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stuff_manager.actioncompletion",
            ),
        ),
        migrations.AlterField(
            model_name="action",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]
