import hashlib,json,time
from django.core import signing
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from django.http.response import HttpResponse
from libs.exceptions import AuthenticationFailed
class TokenAuthtication(BaseAuthentication):
    HEADER = {'typ': 'JWP', 'alg': 'default'}
    KEY = 'KINSON'
    SALT = 'www.wetax.com.cn'
    TIME_OUT = 1440 * 60  # 1 day


    def authenticate(self,request):
        # 支持将Token放入任一位置
        result = False
        if request.META.get("HTTP_AUTHORIZATION"):
            result,username,perms=self.check_token(request.META.get("HTTP_AUTHORIZATION"))
        elif 'token' in request.data:
            result,username,perms=self.check_token(request.data['token'])
        elif 'token' in request.query_params:
            result,username,perms=self.check_token(request.query_params['token'])
        if result:
            return username,perms
        raise AuthenticationFailed()
    
    def encrypt(self,obj):
        """加密"""
        value = signing.dumps(obj, key=self.KEY, salt=self.SALT)
        value = signing.b64_encode(value.encode()).decode()
        return value
    
    
    def decrypt(self,src):
        """解密"""
        src = signing.b64_decode(src.encode()).decode()
        raw = signing.loads(src, key=self.KEY, salt=self.SALT)
        return raw
    
    
    def create_token(self,username,perms):
        """生成token信息"""
        token = cache.get(username)
        if not (token and username ==self.get_payload(token)['username'] and perms == self.get_payload(token)['perms']):
            # 1. 加密头信息
            header = self.encrypt(self.HEADER)
            # 2. 构造Payload
            payload = {
                "username": username,
                "perms": perms,
                "iat": time.time()
            }
            payload = self.encrypt(payload)
            # 3. 生成签名
            md5 = hashlib.md5()
            md5.update(("%s.%s" % (header, payload)).encode())
            signature = md5.hexdigest()
            token = "%s.%s.%s" % (header, payload, signature)
            # 存储到缓存中
            cache.set(username, token, self.TIME_OUT)
        return token
    
    
    def get_payload(self,token):
        try:
            payload = str(token).split('.')[1]
            payload = self.decrypt(payload)
            return payload
        except Exception:
            return False
    
    # 通过token获取用户名
    def get_userinfo(self,token):
        payload = self.get_payload(token)
        if payload:
            return payload['username'],payload['perms']
        else:
            return False,None
    
    # 检查token
    def check_token(self,token):
        username,perms = self.get_userinfo(token)
        if username:
            last_token = cache.get(username)
            if last_token:
                return last_token == token,username,perms
        return False,None,None