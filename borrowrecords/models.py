from django.db import models
from django.utils import timezone
from books.models import Book

class BorrowRecord(models.Model):
    """
    Model representing a book borrowing record in the library system.
    """
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='borrow_records',
        help_text="Book that was borrowed"
    )
    borrowed_by = models.CharField(
        max_length=255, 
        help_text="Name of the person who borrowed the book"
    )
    borrow_date = models.DateField(
        auto_now_add=True, 
        help_text="Date when the book was borrowed"
    )
    return_date = models.DateField(
        null=True, 
        blank=True, 
        help_text="Date when the book was returned (optional)"
    )

    def __str__(self):
        """
        String representation of the BorrowRecord model.
        """
        status = "Returned" if self.return_date else "Not Returned"
        return f"{self.book.title} borrowed by {self.borrowed_by} - {status}"

    def mark_as_returned(self):
        """
        Mark the book as returned and update book's available copies.
        """
        if not self.return_date:
            self.return_date = timezone.now()
            self.save()
            # Increase available copies of the book
            self.book.increase_available_copies()

    @property
    def is_overdue(self):
        """
        Check if the book is overdue (not returned within 14 days).
        """
        if not self.return_date:
            days_borrowed = (timezone.now().date() - self.borrow_date).days
            return days_borrowed > 14
        return False

    class Meta:
        verbose_name = "Borrow Record"
        verbose_name_plural = "Borrow Records"
        ordering = ['-borrow_date']