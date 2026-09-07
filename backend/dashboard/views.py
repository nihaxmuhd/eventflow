from rest_framework.views import APIView
from rest_framework.response import Response

from .selectors import (
    get_dashboard_overview,
)


class DashboardOverviewAPIView(
    APIView
):

    def get(
        self,
        request,
    ):

        return Response(
            get_dashboard_overview()
        )