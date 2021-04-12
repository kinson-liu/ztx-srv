"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include,path
from django.contrib import admin
# from settings.settings import SWITCH
# from rbac import views
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    # path('kinson/',include('kinson.urls')),  
    path('ztx/',include('ztx.urls')),  
    path('rbac/',include('rbac.urls')),  
    path('docs/', include_docs_urls(title="接口文档",
                                    authentication_classes=[], permission_classes=[])),
]
# if SWITCH['AuthMode'] == 'sys' and SWITCH['sysAuth']['AdminBackend']:
#         urlpatterns.append(path('admin/', admin.site.urls))
