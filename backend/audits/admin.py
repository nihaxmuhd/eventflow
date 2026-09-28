from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "school",
        "user",
        "action",
        "entity",
        "entity_id",
        "created_at",
    )

    search_fields = (
        "action",
        "entity",
        "description",
    )

    list_filter = (
        "school",
        "action",
        "entity",
    )

    readonly_fields = (
        "created_at",
    )