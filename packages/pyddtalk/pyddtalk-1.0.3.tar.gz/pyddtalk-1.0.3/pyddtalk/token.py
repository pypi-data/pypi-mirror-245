from weakref import ref
from .base import base
from loguru import logger
import datetime


class token(base):
    def __init__(self, appKey: str, appSecret: str) -> None:
        self.appKey = appKey
        self.appSecret = appSecret
        response = self.get()
        self.token = response.get("accessToken")
        self.expires_in = response.get("expireIn")
        logger.debug(dict(msg="请求的token", token=self.token))

    def get(self):
        api_name = "oauth2/accessToken"
        params = {
            "appKey": self.appKey,
            "appSecret": self.appSecret,
        }
        response = self.request(api_name=api_name, json=params, method="POST")
        return response


class loginToken(base):
    def __init__(
        self,
        clientId: str,
        clientSecret: str,
        code: str,
        refreshToken: str = None,
    ) -> None:
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.code = code
        self.refreshToken = refreshToken

        if self.refreshToken:
            self.grantType = "refresh_token"
        else:
            self.grantType = "authorization_code"
        response = self.get()
        if not response:
            raise Exception("获取token失败")
        self.token = response.get("accessToken")
        self.expires_in = response.get("expireIn")
        self.refreshToken = response.get("refreshToken")
        logger.debug(dict(msg="请求的token", token=self.token))

    def get(self):
        api_name = "oauth2/userAccessToken"
        params = {
            "clientId": self.clientId,
            "clientSecret": self.clientSecret,
            "code": self.code,
            "grantType": self.grantType,
        }
        if self.refreshToken:
            params["refreshToken"] = self.refreshToken
        response = self.request(api_name=api_name, json=params, method="POST")
        return response
