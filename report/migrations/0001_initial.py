# Generated by Django 5.2.1 on 2025-05-09 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReportTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "task_id",
                    models.CharField(db_index=True, max_length=255, unique=True),
                ),
                ("student_id", models.CharField(db_index=True, max_length=64)),
                ("namespace", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("STARTED", "Started"),
                            ("SUCCESS", "Success"),
                            ("FAILURE", "Failure"),
                        ],
                        db_index=True,
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                ("html_report", models.TextField(blank=True, null=True)),
                ("error_message", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
