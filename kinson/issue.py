from libs import iView
from django_filters import FilterSet
from django.db import models
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from libs.exceptions import BusinessException,ParameterException
# Create your views here.

class Issue(models.Model):
    title = models.CharField(max_length=50)
    platform = models.TextField()
    level = models.CharField(max_length=50)
    datetime = models.CharField(max_length=50)
    is_delete = models.BooleanField(default= 0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class IssueFilter(FilterSet):
    class Meta:
        model = Issue
        fields = '__all__'


class issue(iView):
    # 默认认证校验类
    authentication_classes = []
    # 默认权限校验类
    # permission_classes = []
    # 权限校验名称
    perms_map = { 
      'get':    '*',
      'post':   '*',
      'put':    '*',
      'delete': '*'
    }
    # 数据库模型
    queryset = Issue
    # 序列化器
    serializer = IssueSerializer
    # 过滤器
    filter_class = (IssueFilter)

    def get(self,request):
        raise ParameterException()
        return 0