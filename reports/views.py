from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Report
from .serializers import ReportSerializer
from .tasks import generate_library_report

class ReportView(APIView):
    def get(self, request):
        """
        Retrieve the latest report.
        """
        report = Report.objects.order_by('-created_at').first()
        if not report:
            return Response({"error": "No reports available"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Generate a new report using Celery.
        """
        # Trigger the Celery task
        task = generate_library_report.delay()
        return Response({"message": "Report generation initiated", "task_id": task.id}, status=status.HTTP_202_ACCEPTED)
