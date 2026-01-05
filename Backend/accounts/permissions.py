from rest_framework.permissions import BasePermission


CAN_CREATE = {
    "BC": {"PC"},
    "PC": {"TC"},
    "TC": {"CAD"},
}

class MustChangePasswordBlocker(BasePermission):
    """
    Block access to normal endpoints until password changed.
    We'll allow only: me, change-password, logout, refresh.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return True

        if not getattr(user, "must_change_password", False):
            return True

        allowed = {"me", "change_password", "logout", "token_refresh"}
        return getattr(view, "auth_action", "") in allowed


class CanCreateUsers(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        return user.role in CAN_CREATE
