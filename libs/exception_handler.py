import datetime,json,logging,traceback,sys,os
from django.conf import settings
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

# 异常类句柄
def exception_handler(exception, context):
    status = 500
    code = 10000
    msg = '服务器内部错误'
    error_type = exception.__class__.__name__
    if hasattr(exception,'__module__'):
        error_type = exception.__module__+'.'+exception.__class__.__name__
        if exception.__module__ == 'libs.exceptions':
            code=exception.default_code
            msg=exception.default_detail
            status=exception.status_code
    if error_type == 'rest_framework.exceptions.PermissionDenied':
        code=10002
        msg='您没有执行该操作的权限.'
        status=403
    
    request = context['request']
    data = {
        'code':code,
        'msg':msg,
        "@timestamp":str(datetime.datetime.now()),
        "error":error_type,
        "errormsg":str(exception),
        "errorpath":get_error_path(),
        "method":request.method,
        "url":request.path,
        "user":request.user,
        "params":request.query_params,
        "data":request.data,
    }
    
    logger = logging.getLogger('log')
    logger.error(json.dumps(data,ensure_ascii=False))

    if settings.DEBUG:
        return Response(data=data,status = status)
    return ErrorResponse(code= code, msg= msg, status= status)

# 获取错误路径
def get_error_path():
    error_path = []
    traceback_info = traceback.format_exc().split('\n')
    for item in traceback_info:
        if settings.BASE_DIR in item:
            error_path.append(item[2:])
    return error_path

# 异常响应类
class ErrorResponse(HttpResponse):
    def __init__(self, code, msg, data=None, encoder=DjangoJSONEncoder,json_dumps_params=None, **kwargs):
        if json_dumps_params is None:
            json_dumps_params = {}
        kwargs.setdefault('content_type', 'application/json')
        data = {
            "code" : code,
            "msg"  : msg,
            "data" : data
        }
        data = json.dumps(data, cls=encoder, ensure_ascii=False, **json_dumps_params)
        super().__init__(content=data, **kwargs)