from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.db import transaction

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
from common.realtime import has_relevant_changes, publish_event_on_commit


def registration_event_payload(registration):
    return {
        "registration_id": registration.id,
        "event_id": registration.event_id,
        "status": registration.status,
    }


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

        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = request.user.school_id

        serializer = self.get_serializer(data=data)

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
            registration = create_registration(**validated_data)
            publish_event_on_commit(
                event_type="registration.created",
                school_id=registration.school_id,
                payload=registration_event_payload(registration),
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

        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = registration.school_id

        serializer = self.get_serializer(
            registration,
            data=data,
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

        if has_relevant_changes(registration, validated_data):
            with transaction.atomic():
                registration = update_registration(registration, **validated_data)
                publish_event_on_commit(
                    event_type="registration.updated",
                    school_id=registration.school_id,
                    payload=registration_event_payload(registration),
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

        payload = registration_event_payload(registration)
        school_id = registration.school_id
        with transaction.atomic():
            delete_registration(registration)
            publish_event_on_commit(
                event_type="registration.deleted",
                school_id=school_id,
                payload=payload,
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
