from django.urls import path

from .views import (
    SchoolListCreateAPIView,
    SchoolRetrieveUpdateDestroyAPIView,
)

urlpatterns = [

    path(
        "",
        SchoolListCreateAPIView.as_view(),
        name="school-list-create",
    ),

    path(
        "<int:pk>/",
        SchoolRetrieveUpdateDestroyAPIView.as_view(),
        name="school-detail",
    ),

]