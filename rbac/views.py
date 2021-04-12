# from django.contrib.auth.models import User
import json
import logging
# from .models import 
from django.contrib.auth import authenticate
from rest_framework.views import APIView
# from utils.common import JsonResponse
from libs.authtication import TokenAuthtication
from django.core import serializers
from rest_framework.response import Response
from libs.exceptions import LoginFailed,UserNotExist

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
# from django_celery_beat.models import PeriodicTask
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import (FileUploadParser, JSONParser,
                                    MultiPartParser)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from rbac.queryset import get_child_queryset2

from .filters import UserFilter
from .mixins import CreateModelAMixin
from .models import (User, Role, Permission, Organization, RolePerms, UserRoles)
from .permission import RbacPermission, get_permission_list
from .permission_data import RbacFilterSet
from .serializers import (OrganizationSerializer, PermissionSerializer,PositionSerializer, RoleSerializer, 
                          UserCreateSerializer, UserListSerializer,UserModifySerializer)

# Create your views here.
class login(APIView):
    """
    用户登录
    """
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            role_ids = []
            permission_ids = []
            perms = {
                'platform':[],
                'list':[],
                'menu':[],
                'interface':[],
            }
            recv = json.loads(serializers.serialize("json",UserRoles.objects.filter(user_id=user.id)))
            for item in recv:
                role_ids.append(item['fields']['role_id'])
            recv = json.loads(serializers.serialize("json",RolePerms.objects.filter(role_id__in=role_ids)))
            for item in recv:
                permission_ids.append(item['fields']['permission_id'])
            recv = json.loads(serializers.serialize("json",Permission.objects.filter(id__in=permission_ids)))
            for item in recv:
                if item['fields']['type'] == '平台':
                    perms['platform'].append(item['fields']['method'])
                elif item['fields']['type'] == '目录':
                    perms['list'].append(item['fields']['method'])
                elif item['fields']['type'] == '菜单':
                    perms['menu'].append(item['fields']['method'])
                elif item['fields']['type'] == '接口':
                    perms['interface'].append(item['fields']['method'])
            data = {
                "username":user.username,
                "name":user.name,
                "token":TokenAuthtication().create_token(request.data['username'],perms)
            }
            return Response(data= data)
        else:
            raise LoginFailed()


class account(APIView):
    """
    get     获取账户
    post    创建账户
    put     重置账户
    delete  注销账户
    """
    permission_classes = []
    def get(self,request,*args,**kwargs):
        """
        获取账户
        :param  username;
        """
        try:
            user = User.objects.get(username=request.user)
        except Exception:
            raise UserNotExist()
        
        data = {
            "username":user.username,
            "name":user.name,
            "email":user.email,
            "perms":request.auth
        }
        return Response(data= data)


class PermissionViewSet(ModelViewSet):
    """
    权限：增删改查
    """
    perms_map = {'get': '*', 'post': 'perm_create',
                 'put': 'perm_update', 'delete': 'perm_delete'}
    queryset = Permission.objects
    serializer_class = PermissionSerializer
    pagination_class = None
    search_fields = ['name']
    ordering_fields = ['sort']
    ordering = ['pk']


class OrganizationViewSet(ModelViewSet):
    """
    组织机构：增删改查
    """
    test="test"
    perms_map = {'get': '*', 'post': 'org_create',
                 'put': 'org_update', 'delete': 'org_delete'}
    queryset = Organization.objects
    serializer_class = OrganizationSerializer
    pagination_class = None
    search_fields = ['name', 'method']
    ordering_fields = ['pk']
    ordering = ['pk']


class RoleViewSet(ModelViewSet):
    """
    角色：增删改查
    """
    perms_map = {'get': '*', 'post': 'role_create',
                 'put': 'role_update', 'delete': 'role_delete'}
    queryset = Role.objects
    serializer_class = RoleSerializer
    pagination_class = None
    search_fields = ['name']
    ordering_fields = ['pk']
    ordering = ['pk']


class UserViewSet(ModelViewSet):
    """
    用户管理：增删改查
    """
    perms_map = {'get': '*', 'post': '*',
                 'put': 'user_update', 'delete': 'user_delete'}
    queryset = User.objects.order_by('-id')
    serializer_class = UserListSerializer
    filterset_class = UserFilter
    search_fields = ['username', 'name', 'phone', 'email']
    ordering_fields = ['-pk']

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.get_serializer_class(), 'setup_eager_loading'):
            queryset = self.get_serializer_class().setup_eager_loading(queryset)  # 性能优化
        dept = self.request.query_params.get('dept', None)  # 该部门及其子部门所有员工
        if dept is not None:
            deptqueryset = get_child_queryset2(Organization.objects.get(pk=dept))
            queryset = queryset.filter(dept__in=deptqueryset)
        return queryset

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserModifySerializer

    def create(self, request, *args, **kwargs):
        # 创建用户默认添加密码
        password = request.data['password'] if 'password' in request.data else None
        if password:
            password = make_password(password)
        else:
            password = make_password('0000')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(password=password)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, permission_classes=[IsAuthenticated], # perms_map={'put':'change_password'}
            url_name='change_password')
    def password(self, request, pk=None):
        """
        修改密码
        """
        user = User.objects.get(id=pk)
        old_password = request.data['old_password']
        if check_password(old_password, user.password):
            new_password1 = request.data['new_password1']
            new_password2 = request.data['new_password2']
            if new_password1 == new_password2:
                user.set_password(new_password2)
                user.save()
                return Response('密码修改成功!', status=status.HTTP_200_OK)
            else:
                return Response('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('旧密码错误!', status=status.HTTP_400_BAD_REQUEST)

    # perms_map={'get':'*'}, 自定义action控权
    @action(methods=['get'], detail=False, url_name='my_info', permission_classes=[IsAuthenticated])
    def info(self, request, pk=None):
        """
        初始化用户信息
        """
        user = request.user
        perms = get_permission_list(user)
        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'roles': user.roles.values_list('name', flat=True),
            # 'avatar': request._request._current_scheme_host + '/media/' + str(user.image),
            'avatar': user.avatar,
            'perms': perms,
        }
        return Response(data)
