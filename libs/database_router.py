from django.conf import settings
# 数据库自动路由

# https://docs.djangoproject.com/zh-hans/3.1/topics/db/multi-db/#automatic-database-routing
DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING

class DatabaseAppsRouter(object):
    """
    A router to control all database operations on models for different
    databases.
 
    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.
 
    Settings example:
    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    DATABASE_APPS_MAPPING = {'app1': ['readonly':'db1','master':'db2'], 'app2': 'db2'}
    """
 
    def db_for_read(self, model, **hints):
        # 如果根据APP获取的value类型为str，则不分主从
        # 如果存在readonly字段，则返回字段对应的库
        """"Point all read operations to the specific database."""
        if model._meta.app_label in DATABASE_MAPPING:
            if isinstance(DATABASE_MAPPING[model._meta.app_label],str):
                return DATABASE_MAPPING[model._meta.app_label]
            else:
                return DATABASE_MAPPING[model._meta.app_label]['readonly']
        return None
 
    def db_for_write(self, model, **hints):
        # 如果根据APP获取的value类型为str，则不分主从
        # 如果存在master字段，则返回字段对应的库
        """Point all write operations to the specific database."""
        if model._meta.app_label in DATABASE_MAPPING:
            if isinstance(DATABASE_MAPPING[model._meta.app_label],str):
                return DATABASE_MAPPING[model._meta.app_label]
            else:
                return DATABASE_MAPPING[model._meta.app_label]['master']
        return None
 
    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = DATABASE_MAPPING.get(obj1._meta.app_label)
        db_obj2 = DATABASE_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None
 
    def allow_syncdb(self, db, model):
        """Make sure that apps only appear in the related database."""
 
        if db in DATABASE_MAPPING.values():
            return DATABASE_MAPPING.get(model._meta.app_label) == db
        elif model._meta.app_label in DATABASE_MAPPING:
            return False
        return None
 
    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db in DATABASE_MAPPING.values():
            return DATABASE_MAPPING.get(app_label) == db
        elif app_label in DATABASE_MAPPING:
            return False
        return None