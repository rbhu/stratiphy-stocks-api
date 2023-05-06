from rest_framework.permissions import BasePermission
from .models import UserProfile


class IsInvestor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                return user_profile.user_type == 'investor'
            except UserProfile.DoesNotExist:
                return False
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                return user_profile.user_type == 'admin'
            except UserProfile.DoesNotExist:
                return False
        return False
