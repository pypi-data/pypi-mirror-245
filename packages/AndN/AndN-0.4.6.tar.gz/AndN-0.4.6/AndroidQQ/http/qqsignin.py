import requests
import json

from AndroidQQ.http import User_Agent
from AndroidQQ.utils import qq_bkn


def WriteMindJar(cookie: str, skey: str):
    """心灵罐子签到"""
    try:
        response = requests.post(
            url="https://ti.qq.com/qqsignin/mindjar/trpc/WriteMindJar",
            params={
                "bkn": qq_bkn(skey),
            },
            headers={
                "Host": "ti.qq.com",
                "Connection": "keep-alive",
                "Content-Length": "2",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": User_Agent,
                "Content-Type": "application/json",
                "Origin": "https://ti.qq.com",
                "X-Requested-With": "com.tencent.mobileqq",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://ti.qq.com/signin/public/index.html?_wv=1090528161&_wwv=13",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cookie": cookie,
            },
            data=json.dumps({

            })
        )
        return response.json()
    except requests.exceptions.RequestException:
        return {"errcode": -1, "errmsg": '请求异常'}


# if __name__ == '__main__':
