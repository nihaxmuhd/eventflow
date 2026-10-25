from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from django.db import transaction

from .models import House
from .permissions import (
    CanManageHouse,
    CanViewHouse,
)
from .selectors import (
    get_all_houses,
)
from .serializers import HouseSerializer
from .services import (
    create_house,
    update_house,
)

from core.mixins import SchoolFilteredQuerysetMixin
from common.realtime import entity_payload, has_relevant_changes, publish_event_on_commit


@extend_schema(tags=["Houses"])
class HouseListCreateAPIView(
    SchoolFilteredQuerysetMixin,
    ListCreateAPIView,
):

    queryset = get_all_houses()

    serializer_class = HouseSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [CanViewHouse()]

        return [CanManageHouse()]

    def create(self, request, *args, **kwargs):
        # Administrators are always scoped to the school on their account.
        # Supply it before validation because the model relation is required.
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
            house = create_house(**validated_data)
            publish_event_on_commit(
                event_type="house.created",
                school_id=house.school_id,
                payload=entity_payload(house),
            )

        return Response(
            {
                "success": True,
                "message": (
                    "House created successfully."
                ),
                "data": HouseSerializer(
                    house
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Houses"])
class HouseRetrieveUpdateDestroyAPIView(
    SchoolFilteredQuerysetMixin,
    RetrieveUpdateDestroyAPIView,
):

    queryset = House.objects.select_related("school")

    serializer_class = HouseSerializer

    def get_permissions(self):

        if self.request.method == "GET":
            return [CanViewHouse()]

        return [CanManageHouse()]

    def update(self, request, *args, **kwargs):

        house = self.get_object()

        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = house.school_id

        serializer = self.get_serializer(
            house,
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

        changed = has_relevant_changes(house, validated_data)
        if changed:
            with transaction.atomic():
                house = update_house(house, **validated_data)
                publish_event_on_commit(
                    event_type="house.updated",
                    school_id=house.school_id,
                    payload=entity_payload(house),
                )

        return Response(
            {
                "success": True,
                "message": (
                    "House updated successfully."
                ),
                "data": HouseSerializer(
                    house
                ).data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        house = self.get_object()

        if house.students.exists():
            return Response(
                {
                    "success": False,
                    "message": "Cannot delete house. Students are assigned to it.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = entity_payload(house)
        school_id = house.school_id
        with transaction.atomic():
            house.delete()
            publish_event_on_commit(
                event_type="house.deleted", school_id=school_id, payload=payload
            )

        return Response(
            {
                "success": True,
                "message": "House deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
