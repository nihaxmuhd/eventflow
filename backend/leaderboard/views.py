from rest_framework.views import APIView
from rest_framework.response import Response

from .selectors import (
    get_house_leaderboard,
    get_student_leaderboard,
)


class HouseLeaderboardAPIView(
    APIView
):

    def get(
        self,
        request,
    ):

        data = []

        for item in get_house_leaderboard():

            data.append({

                "house_id":
                item[
                    "registration__student__house__id"
                ],

                "house_name":
                item[
                    "registration__student__house__name"
                ],

                "total_points":
                item[
                    "total_points"
                ],

            })

        return Response(
            data
        )


class StudentLeaderboardAPIView(
    APIView
):

    def get(
        self,
        request,
    ):

        data = []

        for item in get_student_leaderboard():

            data.append({

                "student_id":
                item[
                    "registration__student__id"
                ],

                "student_name":
                item[
                    "registration__student__first_name"
                ],

                "total_points":
                item[
                    "total_points"
                ],

            })

        return Response(
            data
        )