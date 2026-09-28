from .models import AuditLog


def create_audit_log(
    *,
    school,
    user,
    action,
    entity,
    entity_id,
    description="",
):

    return AuditLog.objects.create(
        school=school,
        user=user,
        action=action,
        entity=entity,
        entity_id=entity_id,
        description=description,
    )