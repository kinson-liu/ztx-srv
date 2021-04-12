# from django.core.cache import cache
from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    """
    基于角色的权限校验类
    """

    def has_permission(self, request, view):
        """
        权限校验逻辑
        :param request:
        :param view:
        :return:
        """
        if request.auth and 'interface' in request.auth:
            perms = request.auth['interface']
        else:
            perms = []
        # 接口未添加 [perms_map] 变量进行限制,默认全部放行
        if not hasattr(view, 'perms_map'):
            return True
        else:
            perms_map = view.perms_map
            _method = request._request.method.lower()
            if perms_map:
                for key in perms_map:
                    if key == _method or key == '*':
                        if perms_map[key] in perms or perms_map[key] == '*':
                            return True
            return False
    
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True