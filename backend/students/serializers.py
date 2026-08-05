from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    full_name = serializers.ReadOnlyField()

    class Meta:

        model = Student

        fields = (
            "id",
            "school",
            "house",
            "admission_number",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "date_of_birth",
            "class_name",
            "division",
            "parent_name",
            "parent_phone",
            "student_phone",
            "email",
            "address",
            "photo",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "full_name",
        )