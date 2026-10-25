from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from django.db import transaction

from .models import Student
from .permissions import (
    CanManageStudent,
    CanViewStudent,
)
from .selectors import (
    get_all_students,
)
from .serializers import StudentSerializer
from .services import (
    create_student,
    update_student,
    delete_student,
)

from core.mixins import SchoolFilteredQuerysetMixin
from common.realtime import entity_payload, has_relevant_changes, publish_event_on_commit


@extend_schema(tags=["Students"])
class StudentListCreateAPIView(
    SchoolFilteredQuerysetMixin,
    ListCreateAPIView,
):

    queryset = get_all_students()

    serializer_class = StudentSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [CanViewStudent()]

        return [CanManageStudent()]

    def create(self, request, *args, **kwargs):
        # A school administrator's school comes from their authenticated
        # account, never from a client-controlled request field.  It must be
        # present before serializer validation because Student.school is
        # required.
        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = request.user.school_id

        serializer = self.get_serializer(
            data=data
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = (
            serializer.validated_data
        )

        if (
            request.user.role
            != "SUPER_ADMIN"
        ):
            validated_data[
                "school"
            ] = request.user.school

        with transaction.atomic():
            student = create_student(**validated_data)
            publish_event_on_commit(
                event_type="student.created",
                school_id=student.school_id,
                payload=entity_payload(student),
            )

        return Response(
            {
                "success": True,
                "message": (
                    "Student created successfully."
                ),
                "data": StudentSerializer(
                    student
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Students"])
class StudentRetrieveUpdateDestroyAPIView(
    SchoolFilteredQuerysetMixin,
    RetrieveUpdateDestroyAPIView,
):

    queryset = Student.objects.select_related(
        "school",
        "house",
    )

    serializer_class = StudentSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [CanViewStudent()]

        return [CanManageStudent()]

    def update(self, request, *args, **kwargs):

        student = self.get_object()

        # Keep PUT validation and school isolation consistent with create.
        # PATCH callers may omit school, but an administrator must never be
        # able to choose one through the request body.
        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = student.school_id

        serializer = self.get_serializer(
            student,
            data=data,
            partial=request.method == "PATCH",
        )

        serializer.is_valid(
            raise_exception=True
        )

        validated_data = (
            serializer.validated_data
        )

        if (
            request.user.role
            != "SUPER_ADMIN"
        ):
            validated_data.pop(
                "school",
                None,
            )

        changed = has_relevant_changes(student, validated_data)
        if changed:
            with transaction.atomic():
                student = update_student(student, **validated_data)
                publish_event_on_commit(
                    event_type="student.updated",
                    school_id=student.school_id,
                    payload=entity_payload(student),
                )

        return Response(
            {
                "success": True,
                "message": (
                    "Student updated successfully."
                ),
                "data": StudentSerializer(
                    student
                ).data,
            }
        )

    def destroy(self, request, *args, **kwargs):

        student = self.get_object()

        payload = entity_payload(student)
        school_id = student.school_id
        with transaction.atomic():
            delete_student(student)
            publish_event_on_commit(
                event_type="student.deleted", school_id=school_id, payload=payload
            )

        return Response(
            {
                "success": True,
                "message": "Student deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
