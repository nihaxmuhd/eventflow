from .models import (
    Event,
    EventCategory,
)


def get_all_event_categories():

    return (
        EventCategory.objects
        .select_related("school")
        .order_by("name")
    )


def get_event_category_by_id(category_id):

    return (
        EventCategory.objects
        .select_related("school")
        .filter(id=category_id)
        .first()
    )


def get_all_events():

    return (
        Event.objects
        .select_related(
            "school",
            "category",
        )
        .order_by("name")
    )


def get_event_by_id(event_id):

    return (
        Event.objects
        .select_related(
            "school",
            "category",
        )
        .filter(id=event_id)
        .first()
    )


def get_events_by_school(school):

    return (
        Event.objects
        .select_related(
            "school",
            "category",
        )
        .filter(
            school=school,
            status=Event.Status.ACTIVE,
        )
        .order_by("name")
    )