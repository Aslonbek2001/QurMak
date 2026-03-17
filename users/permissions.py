from rest_framework.permissions import BasePermission
from django.utils import timezone

class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user and  request.user.is_authenticated


class IsSelfOrSuperuser(BasePermission):
    """
    Superuser bo'lganlar barcha maydonlarni o'zgartirishlari mumkin.
    Foydalanuvchi o'zi faqat username va password ni o'zgartira oladi.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True  # Superuser hamma maydonni o'zgartirishga ruxsat beradi
        if obj == request.user:
            # Faqat username va password maydonlarini o'zgartirishga ruxsat
            if set(request.data.keys()).issubset({'username', 'password'}):
                return True
        return False