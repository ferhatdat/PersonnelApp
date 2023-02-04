from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission

class IsStaffOrReadOnly(IsAdminUser):
    message = 'Maalesef bu işlem için yetkiniz yoktur!'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)

class IsOwnerAndStafforReadOnly(BasePermission):
    message = 'Maalesef bu işlem için yetkiniz yoktur!'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_staff and (request.user.id == obj.create_user_id))
