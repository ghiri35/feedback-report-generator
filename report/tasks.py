from celery import shared_task, group
from .models import ReportTask
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io, os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def generate_report(self, events, student_id, namespace, content_type):
    report = None
    try:
        report, created = ReportTask.objects.get_or_create(
            task_id=self.request.id,
            student_id=student_id,
            namespace=namespace,
            status="PENDING"
        )
        if not created:
            report.status = "RETRYING"
            report.save()

        # Common logic: sort units and generate event order
        sorted_units = sorted(set(event["unit"] for event in events))
        unit_to_q = {unit: f"Q{i+1}" for i, unit in enumerate(sorted_units)}
        event_order = " -> ".join(unit_to_q[event["unit"]] for event in events)

        content_type = content_type
        if content_type not in {"HTML", "PDF"}:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        file_ext = "html" if content_type == "HTML" else "pdf"

        file_name = f"{student_id}_{self.request.id}.{file_ext}"
        output_path = os.path.join(settings.MEDIA_ROOT, 'reports', file_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.info(f"Generating PDF for student {output_path} and event {content_type}")

        if content_type == "HTML":
            html = f"<h2>Student ID: {student_id}</h2><p>Event Order: {event_order}</p>"

            # Save as HTML file instead of storing in DB
            with open(output_path, 'w',encoding='utf-8') as f:
                f.write(html)
        print("content_type", content_type)
        if content_type == "PDF":
            print("Generating PDF report")
            try:
                c = canvas.Canvas(output_path, pagesize=letter)
                c.drawString(100, 750, f"Student ID: {student_id}")
                c.drawString(100, 730, f"Event Order: {event_order}")
                c.save()

            except Exception as e:
                print("Failed to write file:", e)

        report.file_path.name = f"reports/{file_name}"
        report.file_type = content_type
        report.status = "SUCCESS"
        report.save()
        return report.file_path.url

    except Exception as e:
        if report:
            report.status = "FAILURE"
            report.error_message = str(e)
            report.save()
        raise self.retry(exc=e, countdown=5, max_retries=3)


    
