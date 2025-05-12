from django.db import models

class ReportTask(models.Model):
    TASK_STATUS = [
        ('PENDING', 'Pending'),
        ('STARTED', 'Started'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]

    FILE_TYPE_CHOICES = [
        ('PDF', 'PDF'),
        ('HTML', 'HTML'),
    ]

    task_id = models.CharField(max_length=255, unique=True, db_index=True)
    student_id = models.CharField(max_length=64, db_index=True)
    namespace = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=TASK_STATUS, default='PENDING', db_index=True)

    file_path = models.FileField(upload_to='reports/', null=True, blank=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, null=True, blank=True)
    
    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task_id} - {self.status}"
