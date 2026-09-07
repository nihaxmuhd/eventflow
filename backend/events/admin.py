from django.contrib import admin

from .models import (
    Event,
    EventCategory,
)


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "school",
        "created_at",
    )

    search_fields = (
        "name",
        "school__name",
    )

    list_filter = (
        "school",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "code",
        "school",
        "category",
        "event_type",
        "status",
    )

    search_fields = (
        "name",
        "code",
    )

    list_filter = (
        "school",
        "category",
        "event_type",
        "status",
    )