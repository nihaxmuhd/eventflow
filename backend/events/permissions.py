from rest_framework.permissions import BasePermission

from accounts.models import User


class CanManageEvent(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.role in [
            User.Roles.SUPER_ADMIN,
            User.Roles.ADMIN,
        ]


class CanViewEvent(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.role in [
            User.Roles.SUPER_ADMIN,
            User.Roles.ADMIN,
            User.Roles.MANAGER,
            User.Roles.TEAM_LEADER,
        ]