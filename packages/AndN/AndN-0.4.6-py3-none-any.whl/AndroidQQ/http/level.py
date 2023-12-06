import json
import re

import requests
from bs4 import BeautifulSoup

from AndroidQQ import log

from .headers import *


def qq_level_index(cookie: str):
    """获取QQ等级的具体信息"""
    try:
        response = requests.get(
            url="https://ti.qq.com/qqlevel/index",
            params={
                "_wv": "3",
                "_wwv": "1",
                "tab": "3",
                "source": "26",
            },
            headers={
                "Host": "ti.qq.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": User_Agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                          "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "X-Requested-With": "com.tencent.mobileqq",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cookie": cookie,
            },
        )

        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')
        data_string = None
        for script in scripts:
            if script.string and '__INITIAL_STATE__' in script.string:
                data_string = script.string
                break

        # 提取JavaScript对象

        json_data = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', data_string).group(1)
        json_data = json.loads(json_data)
        return json_data

    except requests.exceptions.RequestException:
        log.error('HTTP 请求失败')
        return {}


if __name__ == '__main__':
    print(qq_level_index())
    pass
