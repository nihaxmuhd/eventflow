from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "admission_number",
        "first_name",
        "last_name",
        "class_name",
        "division",
        "house",
        "school",
        "status",
    )

    list_filter = (
        "school",
        "class_name",
        "division",
        "house",
        "status",
    )

    search_fields = (
        "admission_number",
        "first_name",
        "last_name",
        "parent_name",
        "parent_phone",
    )

    ordering = (
        "admission_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "School Information",
            {
                "fields": (
                    "school",
                    "house",
                ),
            },
        ),

        (
            "Student Information",
            {
                "fields": (
                    "admission_number",
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                    "class_name",
                    "division",
                    "photo",
                    "status",
                ),
            },
        ),

        (
            "Parent Information",
            {
                "fields": (
                    "parent_name",
                    "parent_phone",
                ),
            },
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "student_phone",
                    "email",
                    "address",
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