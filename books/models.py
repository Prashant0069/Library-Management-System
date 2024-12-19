from django.db import models
from django.core.validators import RegexValidator
from authors.models import Author

class Book(models.Model):
    """
    Model representing a book in the library system.
    """
    # ISBN Validator to ensure correct ISBN format
    isbn_validator = RegexValidator(
        regex=r'^\d{10}(\d{3})?$', 
        message="Enter a valid 10 or 13 digit ISBN."
    )

    title = models.CharField(
        max_length=255, 
        help_text="Title of the book"
    )
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="Author of the book"
    )
    isbn = models.CharField(
        max_length=13, 
        unique=True, 
        validators=[isbn_validator],
        help_text="Unique ISBN for the book"
    )
    available_copies = models.IntegerField(
        default=0, 
        help_text="Number of copies available in the library"
    )
    
    def __str__(self):
        """
        String representation of the Book model.
        """
        return f"{self.title} by {self.author.name}"

    def is_available(self):
        """
        Check if the book is available for borrowing.
        """
        return self.available_copies > 0

    def reduce_available_copies(self):
        """
        Reduce available copies when a book is borrowed.
        """
        if self.is_available():
            self.available_copies -= 1
            self.save()
        else:
            raise ValueError("No copies available for borrowing")

    def increase_available_copies(self):
        """
        Increase available copies when a book is returned.
        """
        self.available_copies += 1
        self.save()

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']