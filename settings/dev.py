# 加载公共配置
import os
# 工作目录 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 静态文件目录
STATIC_URL = '/static/'
# 项目秘钥
SECRET_KEY = 'ru8!wpdurq&gfx5d#8qaagh*bqnwhfufeba_%eq0osd+o@kmzt'
# 调试模式
DEBUG = True 

INSTALLED_APPS =  [
    # 'kinson',
    'ztx',
]


# 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'Ops-TopApi',
    #     'USER': 'root',
    #     'PASSWORD': 'root',
    #     'HOST': '10.30.10.28',
    #     'PORT': '3306',
    # },
}
# 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://10.30.10.120:6379/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }
# APP对应的数据库
DATABASE_APPS_MAPPING = {

}