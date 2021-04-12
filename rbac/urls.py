from django.urls import path
from . import views
from django.urls import path, include
from .views import UserViewSet, OrganizationViewSet, PermissionViewSet, RoleViewSet, account, login
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', UserViewSet, basename="user")
router.register('organization', OrganizationViewSet, basename="organization")
router.register('permission', PermissionViewSet, basename="permission")
router.register('role', RoleViewSet, basename="role")
urlpatterns = [
    path('', include(router.urls)),
    path('account',views.account.as_view()),
    path('login',views.login.as_view()),
]