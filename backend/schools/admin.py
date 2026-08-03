from django.contrib import admin

from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "city",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "city",
        "state",
    )

    search_fields = (
        "name",
        "code",
        "email",
        "phone",
    )

    ordering = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "slug",
    )

    fieldsets = (

        (
            "School Information",
            {
                "fields": (
                    "name",
                    "code",
                    "slug",
                    "logo",
                    "status",
                ),
            },
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "phone",
                    "website",
                ),
            },
        ),

        (
            "Address",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                    "pincode",
                ),
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),

    )