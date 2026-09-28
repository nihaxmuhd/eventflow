from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

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

        serializer = self.get_serializer(
            data=request.data
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

        student = create_student(
            **validated_data
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

        serializer = self.get_serializer(
            student,
            data=request.data,
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

        student = update_student(
            student,
            **validated_data,
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

        delete_student(student)

        return Response(
            {
                "success": True,
                "message": "Student deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )