from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)

from .selectors import (
    get_dashboard_overview,
)

from .serializers import (
    DashboardOverviewSerializer,
)


class DashboardOverviewAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
    ):

        school = None

        if (
            request.user.role
            != "SUPER_ADMIN"
        ):
            school = (
                request.user.school
            )

        data = get_dashboard_overview(
            school=school
        )

        serializer = (
            DashboardOverviewSerializer(
                data
            )
        )

        return Response(
            serializer.data
        )