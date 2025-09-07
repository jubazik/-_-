from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
       Permission проверяет, что пользователь является владельцем или админом.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj ==request.user or request.user.is_staff