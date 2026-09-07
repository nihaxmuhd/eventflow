from django.urls import path

from .views import (
    ResultListCreateAPIView,
    ResultRetrieveUpdateDestroyAPIView,
)

urlpatterns = [

    path(
        "",
        ResultListCreateAPIView.as_view(),
        name="result-list-create",
    ),

    path(
        "<int:pk>/",
        ResultRetrieveUpdateDestroyAPIView.as_view(),
        name="result-detail",
    ),

]