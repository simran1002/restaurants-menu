from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Restaurant(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the restaurant")
    address = models.TextField(help_text="Full address of the restaurant")
    phone_number = models.CharField(max_length=20, help_text="Contact phone number")
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Rating from 0.0 to 5.0"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return f"{self.name} - {self.rating}★"
