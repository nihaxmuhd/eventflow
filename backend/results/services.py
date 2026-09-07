from .models import Result


def create_result(
    **data,
):

    return Result.objects.create(
        **data,
    )


def update_result(
    result,
    **data,
):

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