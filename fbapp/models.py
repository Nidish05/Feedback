from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User # Assuming you're using Django's built-in User model

class Feedback(models.Model):
    """
    Django model for user feedback.

    Attributes:
        user (ForeignKey): A foreign key to Django's built-in User model,
                           representing the user who provided the feedback.
                           When the User is deleted, their feedback will also be deleted (CASCADE).
        content (TextField): The text content of the feedback.
        rating (IntegerField): A rating from 1 to 5, validated using MinValueValidator and MaxValueValidator.
        timestamp (DateTimeField): The date and time when the feedback was created.
                                   auto_now_add=True automatically sets this field
                                   to the current datetime when the object is first created.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # If a user is deleted, their feedback is also deleted.
        related_name='feedback_entries', # Allows accessing feedback from a User instance: user.feedback_entries.all()
        help_text="The user who provided this feedback."
    )
    content = models.TextField(
        help_text="The detailed text content of the feedback."
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(5, message="Rating cannot be more than 5.")
        ],
        help_text="A numerical rating from 1 to 5."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, # Automatically sets the creation timestamp.
        help_text="The date and time when the feedback was submitted."
    )

    class Meta:
        """
        Meta options for the Feedback model.
        """
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback Entries"
        ordering = ['-timestamp'] # Default ordering by most recent feedback first.

    def __str__(self):
        """
        String representation of the Feedback object.
        This is what will be displayed in the Django admin and when printing an object.
        """
        return f"Feedback by {self.user.username} - Rating: {self.rating} on {self.timestamp.strftime('%Y-%m-%d')}"

