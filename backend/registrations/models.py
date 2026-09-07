from django.db import models

from schools.models import School
from students.models import Student
from events.models import Event


class Registration(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    registration_number = models.CharField(
        max_length=50,
        unique=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "student",
                    "event",
                ],
                name="unique_student_event_registration",
            ),

        ]

    def __str__(self):

        return (
            f"{self.registration_number} - "
            f"{self.student}"
        )