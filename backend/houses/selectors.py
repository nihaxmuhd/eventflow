from .models import House


def get_all_houses():
    return (
        House.objects
        .select_related("school")
        .order_by("name")
    )


def get_house_by_id(house_id):
    return (
        House.objects
        .select_related("school")
        .filter(id=house_id)
        .first()
    )


def get_houses_by_school(school):
    return (
        House.objects
        .select_related("school")
        .filter(
            school=school,
            status=House.Status.ACTIVE,
        )
        .order_by("name")
    )


def get_house_by_code(school, code):
    return (
        House.objects
        .filter(
            school=school,
            code__iexact=code,
        )
        .first()
    )