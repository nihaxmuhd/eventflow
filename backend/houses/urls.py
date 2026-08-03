from django.urls import path

from .views import (
    HouseListCreateAPIView,
    HouseRetrieveUpdateDestroyAPIView,
)

urlpatterns = [

    path(
        "",
        HouseListCreateAPIView.as_view(),
        name="house-list-create",
    ),

    path(
        "<int:pk>/",
        HouseRetrieveUpdateDestroyAPIView.as_view(),
        name="house-detail",
    ),

]