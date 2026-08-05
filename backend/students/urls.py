from django.urls import path

from .views import (
    StudentListCreateAPIView,
    StudentRetrieveUpdateDestroyAPIView,
)

urlpatterns = [

    path(
        "",
        StudentListCreateAPIView.as_view(),
        name="student-list-create",
    ),

    path(
        "<int:pk>/",
        StudentRetrieveUpdateDestroyAPIView.as_view(),
        name="student-detail",
    ),

]