from rest_framework.exceptions import APIException
from rest_framework import status
# 自定义异常分类
# 框架异常 10001-10999
class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 10001
    default_detail = 'Token认证失败'


# 业务异常 11000-89999
class BusinessException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 11000
    default_detail ='业务异常'
    def __init__(self, default_code=None, default_detail=None):
        if default_code:
            self.default_code = default_code
        if default_detail:
            self.default_detail = default_detail
        super().__init__()

class LoginFailed(BusinessException):
    default_code = 11001
    default_detail = '登录失败，用户名或密码错误'

class UserNotExist(BusinessException):
    default_code = 11002
    default_detail = '获取用户信息失败，无法找到此用户'


# 系统异常 90000-99999
class SystemException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 90000
    default_detail = '系统异常'
    def __init__(self, default_code=None, default_detail=None):
        if default_code:
            self.default_code = default_code
        if default_detail:
            self.default_detail = default_detail
        super().__init__()

class ParameterException(BusinessException):
    default_detail = '参数错误'

class DatabaseException(BusinessException):
    default_detail = '数据库错误'
