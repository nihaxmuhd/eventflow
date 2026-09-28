from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

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

        house = create_house(
            **validated_data
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

        serializer = self.get_serializer(
            house,
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

        house = update_house(
            house,
            **validated_data,
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
                "message": (
                    "Cannot delete house. "
                    "Students are assigned to it."
                ),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    house.delete()

    return Response(
        {
            "success": True,
            "message": "House deleted successfully.",
        },
        status=status.HTTP_204_NO_CONTENT,
    )