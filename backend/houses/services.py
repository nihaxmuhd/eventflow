from .models import House
from .validators import (
    validate_house_name,
    validate_house_code,
)


def create_house(**data):

    validate_house_name(
        school=data["school"],
        name=data["name"],
    )

    validate_house_code(
        school=data["school"],
        code=data["code"],
    )

    return House.objects.create(**data)


def update_house(house, **data):

    validate_house_name(
        school=data.get("school", house.school),
        name=data.get("name", house.name),
        instance=house,
    )

    validate_house_code(
        school=data.get("school", house.school),
        code=data.get("code", house.code),
        instance=house,
    )

    for field, value in data.items():
        setattr(house, field, value)

    house.save()

    return house


def delete_house(house):

    house.delete()