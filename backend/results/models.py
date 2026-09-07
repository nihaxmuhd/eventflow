from django.db import models

from schools.models import School
from events.models import Event
from registrations.models import Registration


class Result(models.Model):

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="results",
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="results",
    )

    registration = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name="results",
    )

    position = models.PositiveIntegerField()

    points = models.PositiveIntegerField()

    remarks = models.TextField(
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
            "position",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "event",
                    "registration",
                ],
                name="unique_result_per_registration",
            ),

            models.UniqueConstraint(
                fields=[
                    "event",
                    "position",
                ],
                name="unique_position_per_event",
            ),

        ]

    def __str__(self):

        return (
            f"{self.event.name} - "
            f"Position {self.position}"
        )