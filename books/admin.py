from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available_copies')
    list_filter = ('author',)
    search_fields = ('title', 'isbn')