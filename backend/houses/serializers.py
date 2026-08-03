from rest_framework import serializers

from .models import House


class HouseSerializer(serializers.ModelSerializer):

    class Meta:

        model = House

        fields = (
            "id",
            "school",
            "name",
            "code",
            "color",
            "logo",
            "description",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )