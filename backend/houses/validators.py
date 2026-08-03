from rest_framework.exceptions import ValidationError

from .models import House


def validate_house_name(school, name, instance=None):
    queryset = House.objects.filter(
        school=school,
        name__iexact=name,
    )

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            {"name": "A house with this name already exists in this school."}
        )


def validate_house_code(school, code, instance=None):
    queryset = House.objects.filter(
        school=school,
        code__iexact=code,
    )

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    if queryset.exists():
        raise ValidationError(
            {"code": "A house with this code already exists in this school."}
        )
    