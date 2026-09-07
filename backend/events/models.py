from django.db import models

# Create your models here.
from django.db import models

from schools.models import School


class EventCategory(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="event_categories",
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
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
                name="unique_event_category_per_school",
            ),

        ]

    def __str__(self):

        return self.name


class Event(models.Model):

    class EventType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        GROUP = "GROUP", "Group"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="events",
    )

    category = models.ForeignKey(
        EventCategory,
        on_delete=models.CASCADE,
        related_name="events",
    )

    name = models.CharField(
        max_length=255,
    )

    code = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True,
    )

    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        default=EventType.INDIVIDUAL,
    )

    max_participants = models.PositiveIntegerField(
        default=1,
    )

    points_1st = models.PositiveIntegerField(
        default=10,
    )

    points_2nd = models.PositiveIntegerField(
        default=5,
    )

    points_3rd = models.PositiveIntegerField(
        default=3,
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
                    "code",
                ],
                name="unique_event_code_per_school",
            ),

        ]

    def __str__(self):

        return self.name