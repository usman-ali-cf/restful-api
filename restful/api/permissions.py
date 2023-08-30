from rest_framework.permissions import BasePermission
from rest_framework import  permissions


class IsOwnerOrReadOnly(BasePermission):
    """
    permission to allow only owner to access snippet
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user
