from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone

class IsActiveClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        current_time = timezone.now()
        
        if not user.is_authenticated:
            raise PermissionDenied(detail="Foydalanuvchi autentifikatsiyadan o'tmagan.")
        
        if user.devise != request.headers.get("devise"):
            raise PermissionDenied(detail="Devise noto'g'ri.")
        
        if current_time >= user.date_end:
            raise PermissionDenied(detail="Muddat tugagan.")
        
        return True


        
        

