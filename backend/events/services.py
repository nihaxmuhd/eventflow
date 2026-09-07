from .models import (
    Event,
    EventCategory,
)


def create_event_category(**data):

    return EventCategory.objects.create(**data)


def update_event_category(
    category,
    **data,
):

    for field, value in data.items():
        setattr(category, field, value)

    category.save()

    return category


def delete_event_category(category):

    category.delete()


def create_event(**data):

    return Event.objects.create(**data)


def update_event(
    event,
    **data,
):

    for field, value in data.items():
        setattr(event, field, value)

    event.save()

    return event


def delete_event(event):

    event.delete()