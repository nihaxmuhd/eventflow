from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Result
from .serializers import ResultSerializer
from .permissions import CanManageResult

from core.mixins import SchoolFilteredQuerysetMixin
from common.realtime import has_relevant_changes, publish_event_on_commit


def result_event_payload(result):
    return {
        "result_id": result.id,
        "event_id": result.event_id,
        "registration_id": result.registration_id,
        "position": result.position,
        "points": result.points,
    }


class ResultListCreateAPIView(
    SchoolFilteredQuerysetMixin,
    generics.ListCreateAPIView,
):

    queryset = Result.objects.select_related(
        "school",
        "event",
        "registration",
    )

    serializer_class = ResultSerializer

    permission_classes = [
        CanManageResult
    ]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = request.user.school_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            result = serializer.save()
            publish_event_on_commit(
                event_type="result.created",
                school_id=result.school_id,
                payload=result_event_payload(result),
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResultRetrieveUpdateDestroyAPIView(
    SchoolFilteredQuerysetMixin,
    generics.RetrieveUpdateDestroyAPIView,
):

    queryset = Result.objects.select_related(
        "school",
        "event",
        "registration",
    )

    serializer_class = ResultSerializer

    permission_classes = [CanManageResult]

    def update(self, request, *args, **kwargs):
        result = self.get_object()
        data = request.data.copy()
        if request.user.role != "SUPER_ADMIN":
            data["school"] = result.school_id
        serializer = self.get_serializer(
            result, data=data, partial=request.method == "PATCH"
        )
        serializer.is_valid(raise_exception=True)

        if has_relevant_changes(result, serializer.validated_data):
            with transaction.atomic():
                result = serializer.save()
                publish_event_on_commit(
                    event_type="result.updated",
                    school_id=result.school_id,
                    payload=result_event_payload(result),
                )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        result = self.get_object()
        payload = result_event_payload(result)
        school_id = result.school_id
        with transaction.atomic():
            result.delete()
            publish_event_on_commit(
                event_type="result.deleted",
                school_id=school_id,
                payload=payload,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
