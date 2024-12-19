from django.db import models

class Author(models.Model):
    """
    Model representing an author in the library system.
    """
    name = models.CharField(
        max_length=255, 
        help_text="Full name of the author"
    )
    bio = models.TextField(
        blank=True, 
        null=True, 
        help_text="Biography of the author"
    )

    def __str__(self):
        """
        String representation of the Author model.
        """
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']