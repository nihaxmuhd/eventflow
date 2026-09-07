from rest_framework import serializers


class HouseLeaderboardSerializer(
    serializers.Serializer
):

    house_id = serializers.IntegerField()

    house_name = serializers.CharField()

    total_points = serializers.IntegerField()


class StudentLeaderboardSerializer(
    serializers.Serializer
):

    student_id = serializers.IntegerField()

    student_name = serializers.CharField()

    total_points = serializers.IntegerField()