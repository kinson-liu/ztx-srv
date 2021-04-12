from rest_framework.views import APIView
from rest_framework.response import Response
from .pagination import CustomPagination
from .filter import CustomFilter

# 继承APIView方法
# 定义默认的模型类、序列化器、搜索器
# 定义默认的REST 请求方法
class iView(APIView):
    # 初始化变量
    # 模型类
    queryset = None
    # 模型类主键
    pk = 'id'
    # 序列化器
    serializer = None
    # 过滤器
    filter_class = None
    # 视图类初始化 
    def __init__(self,**kwargs):
        # 判断模型类中是否有is_delete(软删除)字段。如果有，则启用软删除功能。
        # 即，查询时不显示is_delete=True的数据，删除时设置is_delete为True
        self.soft_delete = hasattr(self.queryset,'is_delete')
        # TODO 添加传入参数校验，为空抛出异常
        super().__init__(**kwargs)
    # Get方法——单查、群查、搜索、排序
    # 单查：id=主键(int)  
    # 群查：id=主键，主键
    def get(self,request):
        # 过滤器
        queryset = CustomFilter().filter_queryset(request=request, queryset=self.queryset.objects.all(), view=self)
        # 分页器
        pg = CustomPagination()
        queryset = pg.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = self.serializer(instance=queryset,many= True)
        return Response(pg.get_paginated_response(serializer.data))
    
    def post(self,request):
        # 如果模型中存在creator字段，且未作为参数传入，则将request.user存入其中
        if 'creator' not in request.data or request.data['creator'] == '':
            request.data['creator'] = request.user
        serializer = self.serializer(data= request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def put(self,request):
        # 如果模型中存在updator字段，且未作为参数传入，则将request.user存入其中
        if 'updator' not in request.data or request.data['updator'] == '':
            request.data['updator'] = request.user
        queryset = self.queryset.objects.get(id= request.data[self.pk])
        serializer = self.serializer(instance=queryset,data= request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def delete(self,request):
        print(request.data[self.pk])
        queryset = self.queryset.objects.get(id= request.data[self.pk])
        # 如果存在软删除字段，则执行软删除逻辑
        if self.soft_delete:
            queryset.is_delete = True
            queryset.save()
        else:
            queryset.delete()
        return Response()