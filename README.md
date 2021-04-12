## DRF-iView

本项目基于 Django RestFramework，在其基础上根据自身需求进行相关改动，实现符合自身需求的框架。

本项目的最终目标是希望将此项目打造成一个对纯对象十分便捷的框架。同时针对特定需求可以重写相关方法实现。相关配置可以通过配置文件或 Apollo 等管理。并将日常调用的方法引入公共类(主要是运维相关)。

**环境依赖：**
基础框架： `djangorestframework`
跨域： `django-cors-headers`
Redis： `django-redis`
MySQL： `mysqlclient`
**项目结构如下：**

    .
    ├── kinson      测试应用
    ├── libs        公共库
    ├── logs        日志输出
    ├── rbac        权限控制
    └── settings    设置
**初始化数据库及数据**

    python manage.py migrate
    python manage.py loaddata initial.json