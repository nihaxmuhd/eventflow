from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(
    serializers.ModelSerializer
):

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    school_name = serializers.CharField(
        source="school.name",
        read_only=True,
    )

    class Meta:

        model = AuditLog

        fields = [
            "id",
            "school",
            "school_name",
            "user",
            "username",
            "action",
            "entity",
            "entity_id",
            "description",
            "created_at",
        ]