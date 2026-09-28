from django.urls import path

from .views import (
    AuditLogListAPIView,
    AuditLogRetrieveAPIView,
)

urlpatterns = [

    path(
        "",
        AuditLogListAPIView.as_view(),
        name="audit-list",
    ),

    path(
        "<int:pk>/",
        AuditLogRetrieveAPIView.as_view(),
        name="audit-detail",
    ),
]