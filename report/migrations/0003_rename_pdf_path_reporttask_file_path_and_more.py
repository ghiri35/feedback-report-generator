# Generated by Django 5.2.1 on 2025-05-10 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("report", "0002_reporttask_pdf_path"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reporttask",
            old_name="pdf_path",
            new_name="file_path",
        ),
        migrations.RemoveField(
            model_name="reporttask",
            name="html_report",
        ),
        migrations.AddField(
            model_name="reporttask",
            name="file_type",
            field=models.CharField(
                blank=True,
                choices=[("PDF", "PDF"), ("HTML", "HTML")],
                max_length=10,
                null=True,
            ),
        ),
    ]
