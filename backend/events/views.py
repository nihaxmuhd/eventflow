from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from common.realtime import entity_payload, has_relevant_changes, publish_event_on_commit
from core.mixins import SchoolFilteredQuerysetMixin
from .models import Event, EventCategory
from .permissions import CanManageEvent
from .serializers import EventSerializer, EventCategorySerializer


class EventCategoryListCreateAPIView(SchoolFilteredQuerysetMixin, generics.ListCreateAPIView):
    queryset = EventCategory.objects.select_related("school")
    serializer_class = EventCategorySerializer
    permission_classes = [CanManageEvent]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = request.user.school_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            category = serializer.save()
            publish_event_on_commit(event_type="event_category.created", school_id=category.school_id,
                payload=entity_payload(category, key="event_category_id"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventCategoryRetrieveUpdateDestroyAPIView(SchoolFilteredQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = EventCategory.objects.select_related("school")
    serializer_class = EventCategorySerializer
    permission_classes = [CanManageEvent]

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = category.school_id
        serializer = self.get_serializer(category, data=data, partial=request.method == "PATCH")
        serializer.is_valid(raise_exception=True)
        if request.user.role != "SUPER_ADMIN":
            serializer.validated_data.pop("school", None)
        if has_relevant_changes(category, serializer.validated_data):
            with transaction.atomic():
                category = serializer.save()
                publish_event_on_commit(event_type="event_category.updated", school_id=category.school_id,
                    payload=entity_payload(category, key="event_category_id"))
        return Response(EventCategorySerializer(category).data)

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        payload = entity_payload(category, key="event_category_id")
        school_id = category.school_id
        with transaction.atomic():
            category.delete()
            publish_event_on_commit(event_type="event_category.deleted", school_id=school_id, payload=payload)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventListCreateAPIView(SchoolFilteredQuerysetMixin, generics.ListCreateAPIView):
    queryset = Event.objects.select_related("school", "category")
    serializer_class = EventSerializer
    permission_classes = [CanManageEvent]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = request.user.school_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            event = serializer.save()
            publish_event_on_commit(event_type="event.created", school_id=event.school_id,
                payload=entity_payload(event, extra={"event_category_id": event.category_id, "status": event.status}))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventRetrieveUpdateDestroyAPIView(SchoolFilteredQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.select_related("school", "category")
    serializer_class = EventSerializer
    permission_classes = [CanManageEvent]

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = event.school_id
        serializer = self.get_serializer(event, data=data, partial=request.method == "PATCH")
        serializer.is_valid(raise_exception=True)
        if request.user.role != "SUPER_ADMIN":
            serializer.validated_data.pop("school", None)
        if has_relevant_changes(event, serializer.validated_data):
            with transaction.atomic():
                event = serializer.save()
                publish_event_on_commit(event_type="event.updated", school_id=event.school_id,
                    payload=entity_payload(event, extra={"event_category_id": event.category_id, "status": event.status}))
        return Response(EventSerializer(event).data)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        payload = entity_payload(event, extra={"event_category_id": event.category_id, "status": event.status})
        school_id = event.school_id
        with transaction.atomic():
            event.delete()
            publish_event_on_commit(event_type="event.deleted", school_id=school_id, payload=payload)
        return Response(status=status.HTTP_204_NO_CONTENT)
