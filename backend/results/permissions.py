from rest_framework.permissions import BasePermission

from accounts.models import User


class CanManageResult(
    BasePermission
):

    def has_permission(
        self,
        request,
        view,
    ):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.user.role in [
            User.Roles.SUPER_ADMIN,
            User.Roles.ADMIN,
        ]