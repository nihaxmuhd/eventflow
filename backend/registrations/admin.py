from django.contrib import admin

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "registration_number",
        "student",
        "event",
        "status",
        "created_at",
    )

    search_fields = (
        "registration_number",
        "student__first_name",
        "student__admission_number",
        "event__name",
    )

    list_filter = (
        "status",
        "school",
        "event",
    )