from django.db.models import Sum

from students.models import Student
from events.models import Event
from registrations.models import Registration
from results.models import Result


def get_dashboard_overview():

    total_students = Student.objects.count()

    total_events = Event.objects.count()

    total_registrations = (
        Registration.objects.count()
    )

    total_results = Result.objects.count()

    house_data = (

        Result.objects

        .values(
            "registration__student__house__name"
        )

        .annotate(
            total_points=Sum("points")
        )

        .order_by(
            "-total_points"
        )

        .first()

    )

    student_data = (

        Result.objects

        .values(
            "registration__student__first_name"
        )

        .annotate(
            total_points=Sum("points")
        )

        .order_by(
            "-total_points"
        )

        .first()

    )

    return {

        "total_students":
        total_students,

        "total_events":
        total_events,

        "total_registrations":
        total_registrations,

        "total_results":
        total_results,

        "top_house":
        house_data[
            "registration__student__house__name"
        ] if house_data else None,

        "top_house_points":
        house_data[
            "total_points"
        ] if house_data else 0,

        "top_student":
        student_data[
            "registration__student__first_name"
        ] if student_data else None,

        "top_student_points":
        student_data[
            "total_points"
        ] if student_data else 0,

    }