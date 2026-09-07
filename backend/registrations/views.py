from rest_framework import generics

from .models import Registration
from .serializers import RegistrationSerializer
from .permissions import CanManageRegistration


class RegistrationListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = Registration.objects.select_related(
        "school",
        "student",
        "event",
    )

    serializer_class = RegistrationSerializer
    permission_classes = [CanManageRegistration]


class RegistrationRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Registration.objects.select_related(
        "school",
        "student",
        "event",
    )

    serializer_class = RegistrationSerializer
    permission_classes = [CanManageRegistration]