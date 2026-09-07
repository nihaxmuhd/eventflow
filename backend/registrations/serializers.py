from rest_framework import serializers

from .models import Registration
from .validators import validate_student_registration


class RegistrationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Registration

        fields = "__all__"

    def validate(self, attrs):

        if self.instance is None:

            validate_student_registration(
                attrs.get("student"),
                attrs.get("event"),
            )

        return attrs