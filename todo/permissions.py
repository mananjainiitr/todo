from .models import project
from todo import models
from rest_framework import permissions

class IsAdminOrMember(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            
            if request.user in obj.member.all():
                return True
            elif request.user.is_admin:
                return True
            elif request.user.email == obj.creator:
                return True
            return False