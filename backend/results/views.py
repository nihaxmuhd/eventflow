from rest_framework import generics

from .models import Result
from .serializers import ResultSerializer
from .permissions import CanManageResult

from core.mixins import SchoolFilteredQuerysetMixin


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

    permission_classes = [CanManageResult]


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