from django.db.models import Sum

from students.models import Student
from events.models import Event
from registrations.models import Registration
from results.models import Result


def get_dashboard_overview(
    school=None,
):

    students = Student.objects.all()
    events = Event.objects.all()
    registrations = Registration.objects.all()
    results = Result.objects.all()

    if school:

        students = students.filter(
            school=school
        )

        events = events.filter(
            school=school
        )

        registrations = registrations.filter(
            school=school
        )

        results = results.filter(
            school=school
        )

    house_data = (
        results
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
        results
        .values(
            "registration__student__first_name",
            "registration__student__last_name",
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
        "total_students": students.count(),
        "total_events": events.count(),
        "total_registrations":
        registrations.count(),
        "total_results":
        results.count(),

        "top_house":
        (
            house_data[
                "registration__student__house__name"
            ]
            if house_data
            else None
        ),

        "top_house_points":
        (
            house_data[
                "total_points"
            ]
            if house_data
            else 0
        ),

        "top_student":
        (
            f"{student_data['registration__student__first_name']} "
            f"{student_data['registration__student__last_name']}"
            if student_data
            else None
        ),

        "top_student_points":
        (
            student_data[
                "total_points"
            ]
            if student_data
            else 0
        ),
    }