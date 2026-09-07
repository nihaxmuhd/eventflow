from django.urls import path

from .views import (
    RegistrationListCreateAPIView,
    RegistrationRetrieveUpdateDestroyAPIView,
)

urlpatterns = [

    path(
        "",
        RegistrationListCreateAPIView.as_view(),
        name="registration-list-create",
    ),

    path(
        "<int:pk>/",
        RegistrationRetrieveUpdateDestroyAPIView.as_view(),
        name="registration-detail",
    ),

]