from django.db import models

from accounts.models import User
from schools.models import School


class AuditLog(models.Model):

    class AuditActions(models.TextChoices):

        CREATE = "CREATE", "Create"
        UPDATE = "UPDATE", "Update"
        DELETE = "DELETE", "Delete"
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"

    class AuditEntities(models.TextChoices):

        SCHOOL = "School", "School"
        HOUSE = "House", "House"
        STUDENT = "Student", "Student"
        CATEGORY = "Category", "Category"
        EVENT = "Event", "Event"
        REGISTRATION = "Registration", "Registration"
        RESULT = "Result", "Result"
        USER = "User", "User"

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="audit_logs",
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=20,
        choices=AuditActions.choices,
    )

    entity = models.CharField(
        max_length=30,
        choices=AuditEntities.choices,
    )

    entity_id = models.PositiveIntegerField()

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return (
            f"{self.action} - "
            f"{self.entity}"
        )