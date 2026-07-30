from rest_framework.permissions import BasePermission

from .models import User


class IsSuperAdmin(BasePermission):
    """
    Allows access only to Super Admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Roles.SUPER_ADMIN
        )


class IsAdmin(BasePermission):
    """
    Allows access only to Admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Roles.ADMIN
        )


class IsManager(BasePermission):
    """
    Allows access only to Manager users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Roles.MANAGER
        )


class IsTeamLeader(BasePermission):
    """
    Allows access only to Team Leader users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Roles.TEAM_LEADER
        )


class IsAdminOrSuperAdmin(BasePermission):
    """
    Allows access to Super Admin and Admin.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Roles.SUPER_ADMIN,
                User.Roles.ADMIN,
            ]
        )


class IsManagerOrAbove(BasePermission):
    """
    Allows access to Super Admin, Admin and Manager.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Roles.SUPER_ADMIN,
                User.Roles.ADMIN,
                User.Roles.MANAGER,
            ]
        )