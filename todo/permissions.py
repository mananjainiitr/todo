from .models import listOfProject, project
from todo import models
from rest_framework import permissions
#if user is admin or creator return true
class IsAdminOrMember(permissions.BasePermission):
        def has_object_permission(self,request,view,obj):
            
            if request.method in permissions.SAFE_METHODS or request.user.admin:
                return True
            if request.user in obj.member.all():
                return True
            elif (obj.creator.email in request.user.email):
                return True

            return False
#if user is admin or creator return true
class IsAdminOrMember_l(permissions.BasePermission):
        def has_object_permission(self,request,view,obj):
            id = obj.project_id.id
            obj = project.objects.get(id = id)
            if request.method in permissions.SAFE_METHODS or request.user.admin:
                return True
            if request.user in obj.member.all():
                return True
            elif (obj.creator.email in request.user.email):
                return True
            return False

#if user is admin or creator return true
class IsAdminOrMember_c(permissions.BasePermission):
        def has_object_permission(self,request,view,obj):
            id = obj.list_id.id
            obj = listOfProject.objects.get(id = id)
            id = obj.project_id.id
            obj = project.objects.get(id = id)
            if request.method in permissions.SAFE_METHODS or request.user.admin:
                return True
            if request.user in obj.member.all():
                return True
            elif (obj.creator.email in request.user.email):
                return True
            return False

#if user is admin return true
class AdminPermition(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.user.admin):
            return True
        return False
#return false always
class NotAcessable(permissions.BasePermission):
    def has_permission(self, request, view):
        return False