from django.db import models

from schools.models import School


class House(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="houses",
    )

    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=20,
    )

    color = models.CharField(
        max_length=7,
        help_text="Hex color (e.g. #FF0000)",
    )

    logo = models.ImageField(
        upload_to="houses/logos/",
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "name",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "school",
                    "name",
                ],
                name="unique_house_name_per_school",
            ),

            models.UniqueConstraint(
                fields=[
                    "school",
                    "code",
                ],
                name="unique_house_code_per_school",
            ),

        ]

    def __str__(self):
        return f"{self.name} ({self.school.name})"