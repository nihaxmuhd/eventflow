from rest_framework import serializers


class DashboardOverviewSerializer(
    serializers.Serializer
):

    total_students = serializers.IntegerField()

    total_events = serializers.IntegerField()

    total_registrations = serializers.IntegerField()

    total_results = serializers.IntegerField()

    top_house = serializers.CharField(
        allow_null=True
    )

    top_house_points = serializers.IntegerField()

    top_student = serializers.CharField(
        allow_null=True
    )

    top_student_points = serializers.IntegerField()