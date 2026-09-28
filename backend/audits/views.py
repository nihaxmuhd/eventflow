from drf_spectacular.utils import extend_schema

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
)

from .models import AuditLog
from .serializers import (
    AuditLogSerializer,
)


@extend_schema(tags=["Audits"])
class AuditLogListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        AuditLogSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = (
            AuditLog.objects
            .select_related(
                "school",
                "user",
            )
        )

        if (
            self.request.user.role
            != "SUPER_ADMIN"
        ):

            queryset = queryset.filter(
                school=
                self.request.user.school
            )

        return queryset


@extend_schema(tags=["Audits"])
class AuditLogRetrieveAPIView(
    generics.RetrieveAPIView
):

    serializer_class = (
        AuditLogSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = (
            AuditLog.objects
            .select_related(
                "school",
                "user",
            )
        )

        if (
            self.request.user.role
            != "SUPER_ADMIN"
        ):

            queryset = queryset.filter(
                school=
                self.request.user.school
            )

        return queryset