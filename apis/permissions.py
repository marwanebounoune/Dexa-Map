from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """permissions to control profiles"""
    def has_object_permission(self, request, view, obj):
        """safe_methods are the get http request without the autorisation of other http request"""
        #if request.method in permissions.SAFE_METHODS:
            #return True
        #if obj i.e the requested user object is equal to the authenticated user 
        return obj.id == request.user.id


class PinPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username.id == request.user.id

#class PhotoPermissions(permissions.BasePermission):
#    def has_object_permission(self, request, view, obj):
#        return obj.pin.id == request.user.id