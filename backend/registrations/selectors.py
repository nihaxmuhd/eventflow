from .models import Registration


def get_all_registrations(
    school=None,
):

    queryset = (
        Registration.objects
        .select_related(
            "school",
            "student",
            "event",
        )
        .order_by(
            "-created_at"
        )
    )

    if school:
        queryset = queryset.filter(
            school=school
        )

    return queryset


def get_registration_by_id(
    registration_id,
):

    return (
        Registration.objects
        .select_related(
            "school",
            "student",
            "event",
        )
        .filter(
            id=registration_id
        )
        .first()
    )