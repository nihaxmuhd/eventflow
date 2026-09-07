from .models import Result


def get_all_results():

    return (
        Result.objects
        .select_related(
            "school",
            "event",
            "registration",
        )
        .order_by(
            "position",
        )
    )


def get_result_by_id(
    result_id,
):

    return (
        Result.objects
        .select_related(
            "school",
            "event",
            "registration",
        )
        .filter(
            id=result_id,
        )
        .first()
    )


def get_results_by_event(
    event,
):

    return (
        Result.objects
        .select_related(
            "registration",
        )
        .filter(
            event=event,
        )
        .order_by(
            "position",
        )
    )