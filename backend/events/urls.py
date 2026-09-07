from django.urls import path

from .views import (
    EventCategoryListCreateAPIView,
    EventCategoryRetrieveUpdateDestroyAPIView,
    EventListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
)

urlpatterns = [

    path(
        "categories/",
        EventCategoryListCreateAPIView.as_view(),
        name="event-category-list-create",
    ),

    path(
        "categories/<int:pk>/",
        EventCategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="event-category-detail",
    ),

    path(
        "",
        EventListCreateAPIView.as_view(),
        name="event-list-create",
    ),

    path(
        "<int:pk>/",
        EventRetrieveUpdateDestroyAPIView.as_view(),
        name="event-detail",
    ),

]