from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
# 分页器
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        # 获取传入参数的分页大小,默认为10
        if self.request.query_params.__contains__(self.page_size_query_param):
            self.page_size = int(self.request.query_params[self.page_size_query_param])
        # 返回特定格式数据
        return Response({
            'total': self.page.paginator.count,
            'pages': (self.page.paginator.count -1) // self.page_size + 1,
            'page_size': self.page_size,
            'results': data
        })