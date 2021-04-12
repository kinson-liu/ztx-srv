from django.db import models
from django.db.models.query import QuerySet
import django.utils.timezone as timezone
# Create your models here.
class SoftDeletableQuerySetMixin(object):
    '''
    QuerySet for SoftDeletableModel. Instead of removing instance sets
    its ``is_deleted`` field to True.
    '''

    def delete(self, soft=True):
        '''
        Soft delete objects from queryset (set their ``is_deleted``
        field to True)
        '''
        if soft:
            self.update(is_deleted=True)
        else:
            return super(SoftDeletableQuerySetMixin, self).delete()


class SoftDeletableQuerySet(SoftDeletableQuerySetMixin, QuerySet):
    pass


class SoftDeletableManagerMixin(object):
    '''
    Manager that limits the queryset by default to show only not deleted
    instances of model.
    '''
    _queryset_class = SoftDeletableQuerySet

    def get_queryset(self, all=False):
        '''
        Return queryset limited to not deleted entries.
        '''
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints
        if all:
            return self._queryset_class(**kwargs)
        return self._queryset_class(**kwargs).filter(is_deleted=False)


class SoftDeletableManager(SoftDeletableManagerMixin, models.Manager):
    pass


class BaseModel(models.Model):
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(
        auto_now=True, verbose_name='修改时间', help_text='修改时间')
    is_deleted = models.BooleanField(
        default=False, verbose_name='删除标记', help_text='删除标记')

    class Meta:
        abstract = True

class SoftModel(BaseModel):
    class Meta:
        abstract = True

    objects = SoftDeletableManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        '''
        这里需要真删除的话soft=False即可
        '''
        if soft:
            self.is_deleted = True
            self.save(using=using)
        else:

            return super(SoftModel, self).delete(using=using, *args, **kwargs)

class Costomer(SoftModel):
    """
    客户
    """
    name = models.CharField('姓名', max_length=20, null=True, blank=True)
    phone = models.CharField('手机号码', max_length=11,
                             null=True, blank=True, unique=False)
    introducer = models.TextField(
        '介绍人', default='/media/default/avatar.png', null=True, blank=True)
    money = models.DecimalField('余额',default=0, decimal_places=2, max_digits=8)
    # dept = models.ForeignKey(
    #     Organization, default=1, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='组织')
    # position = models.ManyToManyField(Position, blank=True, verbose_name='岗位')
    # superior = models.ForeignKey(
    #     'self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='上级主管')
    # roles = models.ManyToManyField(Role, blank=True, verbose_name='角色')

    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name


class Product(SoftModel):
    """
    产品
    """
    name = models.CharField('名称', max_length=50, null=True, blank=True)
    price = models.DecimalField('价格', default=0, decimal_places=2, max_digits=8)
    
    class Meta:
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name


class Income(SoftModel):
    """
    收入
    """
    type_choices = (
        ('赫兹金卡', '赫兹金卡'),
        ('理疗卡', '理疗卡'),
        ('拔罐年卡', '拔罐年卡')
    )
    type = models.CharField('收入类型', max_length=50, choices=type_choices, default='理疗卡')
    costomer = models.ForeignKey(Costomer, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='客户')
    money = models.DecimalField('金额',default=0, decimal_places=2, max_digits=8)
    class Meta:
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Trade(SoftModel):
    """
    交易
    """
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='产品')
    costomer = models.ForeignKey(Costomer, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='客户')
    price = models.DecimalField('价格', default=0, decimal_places=2, max_digits=8)
    amount = models.IntegerField('数量', default=1)

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']