import json
from urllib import parse
import requests

class OAuth:
    def __init__(self, APPID, APPSECRET, CALLBACK):
        self.app_id = APPID
        self.key = APPSECRET
        self.redirect_url = CALLBACK

    def get_auth_url(self):
        params = {
            'client_id': self.app_id,
            'redirect_uri': self.redirect_url,
            'state': 1,
        }
        url = 'https://oauth.yiban.cn/code/html?%s' % parse.urlencode(params)
        return url

    def get_access_token(self, code):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        params = {
            'code': code,
            'client_id': self.app_id,
            'client_secret': self.key,
            'redirect_uri': self.redirect_url,
        }
        url = 'https://oauth.yiban.cn/token/info?%s' % parse.urlencode(params)
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        result = json.loads(response.text)
        access_token = str(result['access_token'])
        self.access_token = access_token
        return access_token

    def get_yb_info(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        params = {
            'access_token': self.access_token,
        }
        url = 'https://openapi.yiban.cn/user/me?%s' % parse.urlencode(params)
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        result = json.loads(response.text)
        return result

