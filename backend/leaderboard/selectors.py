from django.db.models import Sum
from results.models import Result


def get_house_leaderboard(
    school=None,
):

    queryset = Result.objects.all()

    if school:
        queryset = queryset.filter(
            school=school
        )

    return (
        queryset
        .values(
            "registration__student__house__id",
            "registration__student__house__name",
        )
        .annotate(
            total_points=Sum("points")
        )
        .order_by(
            "-total_points"
        )
    )


def get_student_leaderboard(
    school=None,
):

    queryset = Result.objects.all()

    if school:
        queryset = queryset.filter(
            school=school
        )

    return (
        queryset
        .values(
            "registration__student__id",
            "registration__student__first_name",
            "registration__student__last_name",
        )
        .annotate(
            total_points=Sum("points")
        )
        .order_by(
            "-total_points"
        )
    )