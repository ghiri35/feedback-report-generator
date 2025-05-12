from django.urls import path
from .views import  ReportView

urlpatterns = [
    path("assignment/html", ReportView.as_view(), name="generate_html_report"),
    path("assignment/html/<str:task_id>", ReportView.as_view(), name="task_status"),
    path('assignment/pdf', ReportView.as_view(), name='generate_pdf_report'),
    path('assignment/pdf/<str:task_id>', ReportView.as_view(), name='task_status_pdf'),
]
