from .models import Result


def create_result(
    **data,
):

    event = data["event"]

    position = data["position"]

    points = 0

    if position == 1:

        points = event.points_1st

    elif position == 2:

        points = event.points_2nd

    elif position == 3:

        points = event.points_3rd

    data["points"] = points

    return Result.objects.create(
        **data,
    )


def update_result(
    result,
    **data,
):

    if (
        "position" in data
        or "event" in data
    ):

        event = data.get(
            "event",
            result.event,
        )

        position = data.get(
            "position",
            result.position,
        )

        points = 0

        if position == 1:

            points = event.points_1st

        elif position == 2:

            points = event.points_2nd

        elif position == 3:

            points = event.points_3rd

        data["points"] = points

    for field, value in data.items():

        setattr(
            result,
            field,
            value,
        )

    result.save()

    return result


def delete_result(
    result,
):

    result.delete()