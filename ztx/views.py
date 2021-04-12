from rest_framework.viewsets import ModelViewSet
from .models import Costomer, Product, Income, Trade
from .serializers import CostomerSerializer, ProductSerializer, IncomeSerializer, TradeSerializer
from libs import iView
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
from django.db.models import Sum
from datetime import datetime
from datetime import timedelta
# Create your views here.

class CostomerViewSet(ModelViewSet):
    """
    角色：增删改查
    """
    # perms_map = {'get': '*', 'post': 'role_create',
    #              'put': 'role_update', 'delete': 'role_delete'}
    permission_classes = []
    authentication_classes = []
    queryset = Costomer.objects
    serializer_class = CostomerSerializer
    # pagination_class = None
    filter_fields = ('name','introducer')
    search_fields = ('name','introducer')
    ordering_fields = ['pk','create_time']
    ordering = ['-create_time']
class CostomerRecharge(iView):
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

    def get(self,request):
        # 今日 昨日 本周 上周 本月 上月 总计
        # 获取今日收入
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
        # for item in range(11):
        #     now = datetime.strptime('2020-' + str(item+1).zfill(2) + '-01','%Y-%m-%d')
        # 今天
        today  =  now
        print("今天:"+str(today) + ' ' + str(today.weekday()+1))
        # 昨天
        yesterday  =  now - timedelta(days = 1 )
        print("昨天:" + str(yesterday) + ' ' + str(yesterday.weekday()+1))
        # 本周第一天和最后一天
        this_week_start  =  now - timedelta(days = now.weekday())
        this_week_end  =  now  +  timedelta(days = 6 - now.weekday())
        print("本周:" + str(this_week_start) + '——' + str(this_week_end))
        # 上周第一天和最后一天
        last_week_start  =  now - timedelta(days = now.weekday() + 7 )
        last_week_end  =  now - timedelta(days = now.weekday() + 2 )
        print("上周:" + str(last_week_start) + '——' + str(last_week_end))

        # 本月第一天和最后一天
        this_month_start  =  datetime(now.year, now.month,  1 )
        this_month_end  =  datetime(now.year+now.month//12, (now.month)%12+1,  1 )
        # print("本月:" + str(this_month_start) + '——' + str(this_month_end))

        # 上月第一天和最后一天
        # last_month_end  =  this_month_start - timedelta(days = 1 )
        last_month_start  =  datetime((this_month_start - timedelta(days = 1 )).year, (this_month_start - timedelta(days = 1 )).month,  1 )
        last_month_end  =  datetime(now.year, now.month,  1 )
        # print("上月:" + str(last_month_start) + '——' + str(last_month_end))

        # 本季第一天和最后一天
        this_quarter_start  =  datetime(now.year+(now.month+9)//12-1, ((now.month%12//3-1)%4+1)*3,  1 )
        this_quarter_end  =  datetime(now.year+now.month//12, (now.month%12//3+1)*3,  1 )
        # print("本季:" + str(this_quarter_start) + '——' + str(this_quarter_end))

        # 上季第一天和最后一天
        last_quarter_start  =  datetime(now.year+(now.month+6)//12-1, (((now.month+9)%12//3-1)%4+1)*3 ,  1 )
        last_quarter_end  =  this_quarter_start
        # print("上季:" + str(last_quarter_start) + '——' + str(last_quarter_end))

        # 本年第一天和最后一天
        this_year_start  =  datetime(now.year,  1 ,  1 )
        this_year_end  =  datetime(now.year  +  1 ,  1 ,  1 )
        # print("今年:" + str(this_year_start) + '——' + str(this_year_end))

        # 去年第一天和最后一天
        last_year_start  =  datetime((this_year_start - timedelta(days = 1 )).year,  1 ,  1 )
        last_year_end  =  this_year_start
        # print("去年:" + str(last_year_start) + '——' + str(last_year_end))
        
        result = {}
        result['recharge_today']= Income.objects.filter(create_time__date= today).aggregate(sum=Sum("money"))['sum']
        result['recharge_yesterday'] = Income.objects.filter(create_time__date= yesterday).aggregate(sum=Sum("money"))['sum']
        result['recharge_this_week'] = Income.objects.filter(create_time__range= (this_week_start,this_week_end)).aggregate(sum=Sum("money"))['sum']
        result['recharge_last_week'] = Income.objects.filter(create_time__range= (last_week_start,last_week_end)).aggregate(sum=Sum("money"))['sum']
        result['recharge_this_month'] = Income.objects.filter(create_time__range= (this_month_start,this_month_end)).aggregate(sum=Sum("money"))['sum']
        result['recharge_last_month'] = Income.objects.filter(create_time__range= (last_month_start,last_month_end)).aggregate(sum=Sum("money"))['sum']
        result['recharge_this_quarter'] = Income.objects.filter(create_time__range= (this_quarter_start,this_quarter_end)).aggregate(sum=Sum("money"))['sum']
        result['recharge_last_quarter'] = Income.objects.filter(create_time__range= (last_quarter_start,last_quarter_end)).aggregate(sum=Sum("money"))['sum']
        result['recharge_this_year'] = Income.objects.filter(create_time__range= (this_year_start,this_year_end)).aggregate(sum=Sum("money"))['sum']
        result['recharge_last_year'] = Income.objects.filter(create_time__range= (last_year_start,last_year_end)).aggregate(sum=Sum("money"))['sum']
        result['total'] = Income.objects.all().aggregate(sum=Sum("money"))['sum']
        # 校验空数据，并将其设置为0
        for item in result.keys():
            if not result[item]:
                result[item] = 0
        return Response(result)

    def post(self,request):
        costomer = Costomer.objects.get(pk=request.data['id'])
        if request.data['type'] == '理疗卡':
            costomer.money = costomer.money + Decimal(request.data['money'])
            costomer.save()
        Income(type=request.data['type'],money=request.data['money'],costomer= costomer).save()
        return Response()

class CostomerConsume(iView):
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
    # 获取消费统计信息
    def get(self,request):
        trade = Trade.objects.all().aggregate(sum= Sum("product__price"))
        # 今日 昨日 本周 上周 本月 上月 总计
        # 获取今日消费
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
        # for item in range(11):
        #     now = datetime.strptime('2020-' + str(item+1).zfill(2) + '-01','%Y-%m-%d')
        # 今天
        today  =  now
        print("今天:"+str(today) + ' ' + str(today.weekday()+1))
        # 昨天
        yesterday  =  now - timedelta(days = 1 )
        print("昨天:" + str(yesterday) + ' ' + str(yesterday.weekday()+1))
        # 本周第一天和最后一天
        this_week_start  =  now - timedelta(days = now.weekday())
        this_week_end  =  now  +  timedelta(days = 6 - now.weekday())
        print("本周:" + str(this_week_start) + '——' + str(this_week_end))
        # 上周第一天和最后一天
        last_week_start  =  now - timedelta(days = now.weekday() + 7 )
        last_week_end  =  now - timedelta(days = now.weekday() + 2 )
        print("上周:" + str(last_week_start) + '——' + str(last_week_end))

        # 本月第一天和最后一天
        this_month_start  =  datetime(now.year, now.month,  1 )
        this_month_end  =  datetime(now.year+now.month//12, (now.month)%12+1,  1 )
        # print("本月:" + str(this_month_start) + '——' + str(this_month_end))

        # 上月第一天和最后一天
        # last_month_end  =  this_month_start - timedelta(days = 1 )
        last_month_start  =  datetime((this_month_start - timedelta(days = 1 )).year, (this_month_start - timedelta(days = 1 )).month,  1 )
        last_month_end  =  datetime(now.year, now.month,  1 )
        # print("上月:" + str(last_month_start) + '——' + str(last_month_end))

        # 本季第一天和最后一天
        this_quarter_start  =  datetime(now.year+(now.month+9)//12-1, ((now.month%12//3-1)%4+1)*3,  1 )
        this_quarter_end  =  datetime(now.year+now.month//12, (now.month%12//3+1)*3,  1 )
        # print("本季:" + str(this_quarter_start) + '——' + str(this_quarter_end))

        # 上季第一天和最后一天
        last_quarter_start  =  datetime(now.year+(now.month+6)//12-1, (((now.month+9)%12//3-1)%4+1)*3 ,  1 )
        last_quarter_end  =  this_quarter_start
        # print("上季:" + str(last_quarter_start) + '——' + str(last_quarter_end))

        # 本年第一天和最后一天
        this_year_start  =  datetime(now.year,  1 ,  1 )
        this_year_end  =  datetime(now.year  +  1 ,  1 ,  1 )
        # print("今年:" + str(this_year_start) + '——' + str(this_year_end))

        # 去年第一天和最后一天
        last_year_start  =  datetime((this_year_start - timedelta(days = 1 )).year,  1 ,  1 )
        last_year_end  =  this_year_start
        # print("去年:" + str(last_year_start) + '——' + str(last_year_end))
        # Trade.objects.all().aggregate(sum= Sum("product__price"))
        result = {}
        result['consume_today']= Trade.objects.filter(create_time__date= today).aggregate(sum=Sum("product__price"))['sum']
        result['consume_yesterday'] = Trade.objects.filter(create_time__date= yesterday).aggregate(sum=Sum("product__price"))['sum']
        result['consume_this_week'] = Trade.objects.filter(create_time__range= (this_week_start,this_week_end)).aggregate(sum=Sum("product__price"))['sum']
        result['consume_last_week'] = Trade.objects.filter(create_time__range= (last_week_start,last_week_end)).aggregate(sum=Sum("product__price"))['sum']
        result['consume_this_month'] = Trade.objects.filter(create_time__range= (this_month_start,this_month_end)).aggregate(sum=Sum("product__price"))['sum']
        result['consume_last_month'] = Trade.objects.filter(create_time__range= (last_month_start,last_month_end)).aggregate(sum=Sum("product__price"))['sum']
        result['consume_this_quarter'] = Trade.objects.filter(create_time__range= (this_quarter_start,this_quarter_end)).aggregate(sum=Sum("product__price"))['sum']
        result['consume_last_quarter'] = Trade.objects.filter(create_time__range= (last_quarter_start,last_quarter_end)).aggregate(sum=Sum("product__price"))['sum']
        result['consume_this_year'] = Trade.objects.filter(create_time__range= (this_year_start,this_year_end)).aggregate(sum=Sum("product__price"))['sum']
        result['consume_last_year'] = Trade.objects.filter(create_time__range= (last_year_start,last_year_end)).aggregate(sum=Sum("product__price"))['sum']
        result['total'] = Trade.objects.filter().aggregate(sum=Sum("product__price"))['sum']
        # 校验空数据，并将其设置为0
        for item in result.keys():
            if not result[item]:
                result[item] = 0
        return Response(result)
    def post(self,request):
        # 1. 添加消费记录
        # 2. 修改用户余额
        costomer = Costomer.objects.get(pk=request.data['id'])
        product = Product.objects.get(pk=request.data['product_id'])
        costomer.money = costomer.money - Decimal(request.data['price'])
        costomer.save()
        Trade(costomer= costomer, product= product,price= request.data['price'],amount=request.data['amount']).save()
        return Response()

class ProductViewSet(ModelViewSet):
    """
    角色：增删改查
    """
    perms_map = {'get': '*', 'post': '*',
                 'put': '*', 'delete': '*'}
    permission_classes = []
    authentication_classes = []
    queryset = Product.objects
    serializer_class = ProductSerializer
    # pagination_class = None
    search_fields = ['name']
    ordering_fields = ['pk']
    ordering = ['pk']

class IncomeViewSet(ModelViewSet):
    """
    角色：增删改查
    """
    # perms_map = {'get': '*', 'post': 'role_create',
    #              'put': 'role_update', 'delete': 'role_delete'}
    permission_classes = []
    authentication_classes = []
    queryset = Income.objects
    serializer_class = IncomeSerializer
    # pagination_class = None
    # search_fields = ['costomer']
    ordering_fields = ['pk','create_time']
    ordering = ['-create_time']
    filterset_fields = ['costomer_id']


class TradeViewSet(ModelViewSet):
    """
    角色：增删改查
    """
    # perms_map = {'get': '*', 'post': 'role_create',
    #              'put': 'role_update', 'delete': 'role_delete'}
    permission_classes = []
    authentication_classes = []
    queryset = Trade.objects
    serializer_class = TradeSerializer
    # pagination_class = None
    # search_fields = ['costomer']
    ordering_fields = ['pk','create_time']
    ordering = ['-create_time']
    filterset_fields = ['costomer_id']