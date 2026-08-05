from .models import Student


def get_all_students():
    return (
        Student.objects
        .select_related(
            "school",
            "house",
        )
        .order_by("admission_number")
    )


def get_student_by_id(student_id):
    return (
        Student.objects
        .select_related(
            "school",
            "house",
        )
        .filter(id=student_id)
        .first()
    )


def get_students_by_school(school):
    return (
        Student.objects
        .select_related(
            "school",
            "house",
        )
        .filter(
            school=school,
            status=Student.Status.ACTIVE,
        )
        .order_by("admission_number")
    )


def get_student_by_admission_number(
    school,
    admission_number,
):
    return (
        Student.objects
        .select_related(
            "school",
            "house",
        )
        .filter(
            school=school,
            admission_number__iexact=admission_number,
        )
        .first()
    )