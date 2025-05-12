from django.shortcuts import render
from django.http import FileResponse
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ReportTask
from .tasks import generate_report
from celery.result import AsyncResult
import os
import logging

logger = logging.getLogger(__name__)


class ReportView(APIView):

    def get(self, request, task_id):
        path = request.path.lower()
        report_type = 'PDF' if 'pdf' in path else 'HTML'

        task = AsyncResult(task_id)

        if task.state == 'PENDING':
            return Response({"status": "PENDING"}, status=status.HTTP_202_ACCEPTED)

        elif task.state == 'SUCCESS':
            try:
                report = ReportTask.objects.get(task_id=task_id)

                if report.file_type != report_type:
                    return Response({"error": f"Task did not generate a {report_type} report."}, status=status.HTTP_400_BAD_REQUEST)
                
                if report.file_path:
                    full_path = report.file_path.path
                    print(full_path)
                    if not os.path.exists(full_path):
                        return Response({"error": f"{report_type} file not found."}, status=status.HTTP_404_NOT_FOUND)
                    
                    return FileResponse(
                                open(full_path, 'rb'),
                                content_type=f'application/{report_type.lower()}',
                                as_attachment=True,
                                filename=os.path.basename(full_path)
                                )

                else:
                    return Response({"error": f"{report_type} not found."}, status=status.HTTP_404_NOT_FOUND)
            except ReportTask.DoesNotExist:
                return Response({"error": "Task not found in DB"}, status=status.HTTP_404_NOT_FOUND)

        elif task.state == 'FAILURE':
            return Response({
                "status": "FAILED",
                "error_message": str(task.info) if task.info else "Unknown error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"status": f"Task state: {task.state}"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        path = request.path.lower()
        report_type = 'PDF' if 'pdf' in path else 'HTML'

        print("report_type", report_type)
        payload = request.data
        if not isinstance(payload, list) or not payload:
            return Response({"error": "Invalid input format"}, status=status.HTTP_400_BAD_REQUEST)

        response_data = []
        for student_info in payload:
            student_id = student_info.get("student_id")
            namespace = student_info.get("namespace")
            events = student_info.get("events", [])

            if not student_id or not events:
                return Response({"error": "Missing student_id or events"}, status=status.HTTP_400_BAD_REQUEST)
            
            task = generate_report.delay(events, student_id, namespace, report_type)  
            response_data.append({
                "student_id": student_id,
                "task_id": task.id
            })
        if not response_data:
            return Response({"error": "No valid student data provided."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status=status.HTTP_202_ACCEPTED)

