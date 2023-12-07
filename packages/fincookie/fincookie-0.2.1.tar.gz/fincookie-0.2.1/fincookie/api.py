import requests
import socket
import re

cloud_cloud_api = f"http://10.55.3.250/cookieService/"
cloud_local_api = "http://hive.finchina.local/api/hwy/cookieService/"
local_local_api = "http://10.17.214.105/"  # 等待服务器申请完成后修改
dev_api = "http://10.17.214.105/"

MODE = 'USER'


def set_dev(dev: bool = True):
    global MODE
    if dev is True:
        MODE = 'DEVELOPER'
    else:
        MODE = "USER"


def get_cookies(appid: str,
                get_last: int = 0,
                block_timeout: int = 0,
                proxy: str = None,
                url: str = None,
                url_timeout: int = None,
                script: str = None,
                wait_for: str = None,
                wait_timeout: int = None,
                selector: str = None,
                state: str = None,
                action: str = None,
                type_string: str = None,
                renew_interval: int = 3000,
                match_proxy: bool = False) -> dict:
    data = {k: v for k, v in locals().items() if isinstance(v, (int, str))}
    ip = socket.gethostbyname(socket.gethostname())
    api = dev_api if MODE == 'DEVELOPER' else cloud_cloud_api if ip[:5] == '10.55' else local_local_api if match_proxy else cloud_local_api
    json_data = requests.post(api, data=data).json()
    return json_data


def get_logs(appid: str = None, date_from: str = None, request_id: str = None):
    logs = ""
    params = "?"
    params += f'appid={appid}&' if appid else ''
    params += f'from={date_from}&' if date_from else ''
    params += f'request={request_id}' if request_id else ''
    ip = socket.gethostbyname(socket.gethostname())
    if MODE == 'DEVELOPER':
        apis = [dev_api]
    else:
        apis = [cloud_cloud_api if ip[:5] == '10.55' else cloud_local_api, local_local_api]
    for api in apis:
        api = api + 'get_logs' + params
        res = requests.get(api)
        logs += (res.text + "<br>") if '20' in res.text else ''
    return '无相关日志' if logs == '' else logs.replace('<br>', '\n')


def get_loads():
    loads = {}
    ip = socket.gethostbyname(socket.gethostname())
    if MODE == 'DEVELOPER':
        apis = [dev_api]
    else:
        apis = [cloud_cloud_api if ip[:5] == '10.55' else cloud_local_api, local_local_api]
    for api in apis:
        api = api + "get_loads"
        res = requests.get(api)
        loads.update(res.json())
    return loads


def cookie_format(cookies: dict or str):
    if cookies is None:
        return ''
    if isinstance(cookies, dict):
        return "; ".join([f"{key}={value}" for key, value in cookies.items()])
    else:
        return dict([(item.split("=", 1)[0].strip(), item.split("=", 1)[1].strip()) for item in cookies.split(";")])


def headers_format(headers: dict or str):
    if headers is None:
        return None
    if isinstance(headers, dict):
        return "\n".join([f"{key}: {value}" for key, value in headers.items()])
    else:
        return dict([(item.split(":", 1)[0].strip(), item.split(":", 1)[1].strip()) for item in headers.split("\n")])


def proxy_format(proxy: str):
    return {"http": proxy, "https": proxy}


if __name__ == '__main__':
    # print(get_logs('1234567', date_from='2020-01-01'))
    print(get_loads())
