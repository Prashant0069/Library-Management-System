from django.contrib import admin
from .models import BorrowRecord

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrowed_by', 'borrow_date', 'return_date')
    list_filter = ('return_date',)
    search_fields = ('book__title', 'borrowed_by')