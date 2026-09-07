from rest_framework import generics

from .models import School
from .serializers import SchoolSerializer


class SchoolListCreateAPIView(
    generics.ListCreateAPIView
):

    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = School.objects.all()
    serializer_class = SchoolSerializer