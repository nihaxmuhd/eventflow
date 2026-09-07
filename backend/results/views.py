from rest_framework import generics

from .models import Result
from .serializers import ResultSerializer
from .permissions import CanManageResult


class ResultListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = Result.objects.select_related(
        "school",
        "event",
        "registration",
    )

    serializer_class = ResultSerializer
    permission_classes = [CanManageResult]


class ResultRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Result.objects.select_related(
        "school",
        "event",
        "registration",
    )

    serializer_class = ResultSerializer
    permission_classes = [CanManageResult]