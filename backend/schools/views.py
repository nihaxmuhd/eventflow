from rest_framework import generics
from django.db import transaction

from .models import School
from .serializers import SchoolSerializer
from .permissions import IsSuperAdmin

from audits.services import create_audit_log
from audits.models import AuditLog
from common.realtime import entity_payload, has_relevant_changes, publish_event_on_commit


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

        with transaction.atomic():
            school = serializer.save()
            create_audit_log(school=school, user=self.request.user,
                action=AuditLog.AuditActions.CREATE, entity=AuditLog.AuditEntities.SCHOOL,
                entity_id=school.id, description=f"Created school {school.name}")
            publish_event_on_commit(event_type="school.created", school_id=school.id,
                payload=entity_payload(school))


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

        if not has_relevant_changes(serializer.instance, serializer.validated_data):
            return
        with transaction.atomic():
            school = serializer.save()
            create_audit_log(school=school, user=self.request.user,
                action=AuditLog.AuditActions.UPDATE, entity=AuditLog.AuditEntities.SCHOOL,
                entity_id=school.id, description=f"Updated school {school.name}")
            publish_event_on_commit(event_type="school.updated", school_id=school.id,
                payload=entity_payload(school))

    def perform_destroy(
        self,
        instance,
    ):

        school_name = instance.name
        school_id = instance.id

        with transaction.atomic():
            create_audit_log(school=instance, user=self.request.user,
                action=AuditLog.AuditActions.DELETE, entity=AuditLog.AuditEntities.SCHOOL,
                entity_id=school_id, description=f"Deleted school {school_name}")
            instance.delete()
            publish_event_on_commit(event_type="school.deleted", school_id=school_id,
                payload={"school_id": school_id})
