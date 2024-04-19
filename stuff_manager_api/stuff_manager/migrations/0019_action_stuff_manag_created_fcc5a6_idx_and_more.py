# Generated by Django 5.0.1 on 2024-04-19 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stuff_manager", "0018_unprocessed_created"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="action",
            index=models.Index(
                fields=["created"], name="stuff_manag_created_fcc5a6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="action",
            index=models.Index(
                fields=["created", "title"], name="stuff_manag_created_6e8dac_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="action",
            index=models.Index(
                fields=["created", "energy"], name="stuff_manag_created_8eeab9_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="action",
            index=models.Index(fields=["energy"], name="stuff_manag_energy_baeb6a_idx"),
        ),
        migrations.AddIndex(
            model_name="action",
            index=models.Index(fields=["title"], name="stuff_manag_title_a53497_idx"),
        ),
        migrations.AddIndex(
            model_name="action",
            index=models.Index(
                fields=["project"], name="stuff_manag_project_f3229e_idx"
            ),
        ),
    ]
