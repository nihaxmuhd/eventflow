from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "profile_image",
        )

    def get_profile_image(self, obj):
        request = self.context.get("request")

        if obj.profile_image:
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url

        return None



class LoginSerializer(serializers.Serializer):

    login = serializers.CharField(
        max_length=150,
        required=True,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField(required=True)