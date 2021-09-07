from .models import project
from todo import models
from rest_framework import permissions

class IsAdminOrMember(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            check = models.project.objects.get(id=obj)
            if request.user in check.member.all():
                return True
            elif request.user.is_admin:
                return True
            return False