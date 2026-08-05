from django.db import models

from schools.models import School
from houses.models import House


class Student(models.Model):

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        ALUMNI = "ALUMNI", "Alumni"

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="students",
    )

    house = models.ForeignKey(
        House,
        on_delete=models.SET_NULL,
        related_name="students",
        null=True,
        blank=True,
    )

    admission_number = models.CharField(
        max_length=50,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    class_name = models.CharField(
        max_length=20,
    )

    division = models.CharField(
        max_length=10,
    )

    parent_name = models.CharField(
        max_length=150,
        blank=True,
    )

    parent_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    student_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    photo = models.ImageField(
        upload_to="students/photos/",
        blank=True,
        null=True,
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
            "admission_number",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "school",
                    "admission_number",
                ],
                name="unique_student_admission_per_school",
            ),

        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.admission_number} - {self.full_name}"