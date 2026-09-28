from rest_framework import generics

from .models import School
from .serializers import SchoolSerializer
from .permissions import IsSuperAdmin

from audits.services import create_audit_log
from audits.models import AuditLog


class SchoolListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsSuperAdmin]

    def perform_create(
        self,
        serializer,
    ):

        school = serializer.save()

        create_audit_log(
            school=school,
            user=self.request.user,
            action=AuditLog.AuditActions.CREATE,
            entity=AuditLog.AuditEntities.SCHOOL,
            entity_id=school.id,
            description=(
                f"Created school "
                f"{school.name}"
            ),
        )


class SchoolRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsSuperAdmin]

    def perform_update(
        self,
        serializer,
    ):

        school = serializer.save()

        create_audit_log(
            school=school,
            user=self.request.user,
            action=AuditLog.AuditActions.UPDATE,
            entity=AuditLog.AuditEntities.SCHOOL,
            entity_id=school.id,
            description=(
                f"Updated school "
                f"{school.name}"
            ),
        )

    def perform_destroy(
        self,
        instance,
    ):

        school_name = instance.name
        school_id = instance.id

        create_audit_log(
            school=instance,
            user=self.request.user,
            action=AuditLog.AuditActions.DELETE,
            entity=AuditLog.AuditEntities.SCHOOL,
            entity_id=school_id,
            description=(
                f"Deleted school "
                f"{school_name}"
            ),
        )

        instance.delete()