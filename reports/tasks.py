import os
import json
from datetime import datetime
from celery import shared_task
from django.conf import settings
from authors.models import Author
from books.models import Book
from borrowrecords.models import BorrowRecord
import logging

logger = logging.getLogger(__name__)

@shared_task
def generate_library_report():
    """
    Generate a comprehensive library report
    """
    try:
        report_data = {
            'total_authors': Author.objects.count(),
            'total_books': Book.objects.count(),
            'total_borrowed_books': BorrowRecord.objects.filter(return_date__isnull=True).count(),
            'generated_at': datetime.now().isoformat()
        }
        
        reports_dir = os.path.abspath(settings.REPORTS_DIR)
        print(f"Reports directory path: {reports_dir}")
        
        os.makedirs(reports_dir, exist_ok=True)
        
        filename = f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        filepath = os.path.join(reports_dir, filename)
        print(f"Attempting to write report to: {filepath}")
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=4)
        
        print(f"Successfully wrote report to: {filepath}")
        
        if os.path.exists(filepath):
            print("File verification successful")
        else:
            print("File was not created successfully")
            
        return filepath
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        raise
    