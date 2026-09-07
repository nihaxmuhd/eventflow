from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "event",
        "registration",
        "position",
        "points",
        "created_at",
    )

    search_fields = (
        "event__name",
        "registration__registration_number",
    )

    list_filter = (
        "school",
        "event",
    )