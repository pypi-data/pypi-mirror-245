from loguru import logger
import requests


class User:
    def __init__(self, token: str) -> None:
        self.token = token

    def token2userInfo(self, unionId="me"):
        url = f"https://api.dingtalk.com/v1.0/contact/users/{unionId}"
        headers = {"x-acs-dingtalk-access-token": self.token}
        response = requests.get(
            url,
            headers=headers,
        )
        if response.status_code != 200:
            logger.error(dict(msg="请求错误", data=response.json()))
            raise Exception("请求错误")
        return response.json()
