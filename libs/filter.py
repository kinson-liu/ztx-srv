from django_filters.rest_framework import DjangoFilterBackend
# 默认APIView不支持Filter 因此，使用如下类作为默认过滤类，详情查看下方文档
# https://stackoverflow.com/questions/43906253/django-filter-on-apiview
class CustomFilter(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # 获取该类的过滤器
        filter_class = self.get_filter_class(view, queryset)
        # 如果获取成功，返回添加完过滤条件的模型类
        if filter_class:
            # 单查 OR 群查？
            # 检查传入参数中是否包含主键
            if request.query_params.__contains__(view.pk):
                # 检查主键是否存在多个
                if ',' in request.query_params[view.pk]:
                    queryset = queryset.filter(pk__in=request.query_params[view.pk].split(','))
                else:
                    queryset = queryset.filter(pk=request.query_params[view.pk])
            # 排序
            if 'ordering' in request.query_params:
                ordering = request.query_params['ordering'].split(',')
            else:
                ordering = ['id']
            queryset = queryset.order_by(*ordering)
            # 不显示软删除字段
            if view.soft_delete:
                queryset = queryset.filter(is_delete=False)
            # 自定义过滤器
            return filter_class(request.query_params, queryset=queryset, request=request).qs
        # 未获取到，则原样返回
        return queryset
