from rest_framework import generics

from .models import Registration
from .serializers import RegistrationSerializer
from .permissions import CanManageRegistration

from core.mixins import SchoolFilteredQuerysetMixin


class RegistrationListCreateAPIView(
    SchoolFilteredQuerysetMixin,
    generics.ListCreateAPIView,
):

    queryset = Registration.objects.select_related(
        "school",
        "student",
        "event",
    )

    serializer_class = RegistrationSerializer

    permission_classes = [CanManageRegistration]


class RegistrationRetrieveUpdateDestroyAPIView(
    SchoolFilteredQuerysetMixin,
    generics.RetrieveUpdateDestroyAPIView,
):

    queryset = Registration.objects.select_related(
        "school",
        "student",
        "event",
    )

    serializer_class = RegistrationSerializer

    permission_classes = [CanManageRegistration]