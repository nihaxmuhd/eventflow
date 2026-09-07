from rest_framework import generics

from .models import Event, EventCategory
from .permissions import CanManageEvent
from .serializers import (
    EventSerializer,
    EventCategorySerializer,
)


class EventCategoryListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [CanManageEvent]


class EventCategoryRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [CanManageEvent]


class EventListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = Event.objects.select_related(
        "school",
        "category",
    )

    serializer_class = EventSerializer
    permission_classes = [CanManageEvent]


class EventRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Event.objects.select_related(
        "school",
        "category",
    )

    serializer_class = EventSerializer
    permission_classes = [CanManageEvent]