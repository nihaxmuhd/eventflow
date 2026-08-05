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


@extend_schema(tags=["Students"])
class StudentListCreateAPIView(ListCreateAPIView):

    serializer_class = StudentSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [CanViewStudent()]

        return [CanManageStudent()]

    def get_queryset(self):

        return get_all_students()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = create_student(
            **serializer.validated_data,
        )

        return Response(
            {
                "success": True,
                "message": "Student created successfully.",
                "data": StudentSerializer(student).data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Students"])
class StudentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

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

        serializer.is_valid(raise_exception=True)

        student = update_student(
            student,
            **serializer.validated_data,
        )

        return Response(
            {
                "success": True,
                "message": "Student updated successfully.",
                "data": StudentSerializer(student).data,
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