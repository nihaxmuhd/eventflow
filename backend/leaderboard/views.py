from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)

from .selectors import (
    get_house_leaderboard,
    get_student_leaderboard,
)

from .serializers import (
    HouseLeaderboardSerializer,
    StudentLeaderboardSerializer,
)


class HouseLeaderboardAPIView(
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

        leaderboard = []

        for index, item in enumerate(
            get_house_leaderboard(
                school
            ),
            start=1,
        ):

            leaderboard.append(
                {
                    "rank": index,
                    "house_id": item[
                        "registration__student__house__id"
                    ],
                    "house_name": item[
                        "registration__student__house__name"
                    ],
                    "total_points": item[
                        "total_points"
                    ],
                }
            )

        serializer = (
            HouseLeaderboardSerializer(
                leaderboard,
                many=True,
            )
        )

        return Response(
            serializer.data
        )


class StudentLeaderboardAPIView(
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

        leaderboard = []

        for index, item in enumerate(
            get_student_leaderboard(
                school
            ),
            start=1,
        ):

            leaderboard.append(
                {
                    "rank": index,
                    "student_id": item[
                        "registration__student__id"
                    ],
                    "student_name":
                    (
                        f"{item['registration__student__first_name']} "
                        f"{item['registration__student__last_name']}"
                    ),
                    "total_points": item[
                        "total_points"
                    ],
                }
            )

        serializer = (
            StudentLeaderboardSerializer(
                leaderboard,
                many=True,
            )
        )

        return Response(
            serializer.data
        )