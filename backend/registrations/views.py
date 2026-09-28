from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .models import Registration
from .serializers import RegistrationSerializer
from .permissions import CanManageRegistration

from .services import (
    create_registration,
    update_registration,
    delete_registration,
)

from core.mixins import (
    SchoolFilteredQuerysetMixin,
)


class RegistrationListCreateAPIView(
    SchoolFilteredQuerysetMixin,
    generics.ListCreateAPIView,
):

    queryset = Registration.objects.select_related(
        "school",
        "student",
        "event",
    )

    serializer_class = (
        RegistrationSerializer
    )

    permission_classes = [
        CanManageRegistration
    ]

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

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

        registration = (
            create_registration(
                **validated_data
            )
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Registration "
                    "created successfully."
                ),
                "data": (
                    RegistrationSerializer(
                        registration
                    ).data
                ),
            },
            status=status.HTTP_201_CREATED,
        )


class RegistrationRetrieveUpdateDestroyAPIView(
    SchoolFilteredQuerysetMixin,
    generics.RetrieveUpdateDestroyAPIView,
):

    queryset = Registration.objects.select_related(
        "school",
        "student",
        "event",
    )

    serializer_class = (
        RegistrationSerializer
    )

    permission_classes = [
        CanManageRegistration
    ]

    def update(
        self,
        request,
        *args,
        **kwargs,
    ):

        registration = (
            self.get_object()
        )

        serializer = self.get_serializer(
            registration,
            data=request.data,
            partial=(
                request.method
                == "PATCH"
            ),
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

        registration = (
            update_registration(
                registration,
                **validated_data,
            )
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Registration "
                    "updated successfully."
                ),
                "data": (
                    RegistrationSerializer(
                        registration
                    ).data
                ),
            }
        )

    def destroy(
        self,
        request,
        *args,
        **kwargs,
    ):

        registration = (
            self.get_object()
        )

        delete_registration(
            registration
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Registration "
                    "deleted successfully."
                ),
            },
            status=status.HTTP_204_NO_CONTENT,
        )