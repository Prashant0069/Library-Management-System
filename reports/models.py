from django.db import models
from datetime import datetime

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"Report {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
