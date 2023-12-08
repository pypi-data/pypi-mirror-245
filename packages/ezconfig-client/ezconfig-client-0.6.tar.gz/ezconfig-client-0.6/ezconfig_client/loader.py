# 获取几个环境变量
# EZCONFIG_ENV
# EZCONFIG_APPID
# EZCONFIG_SECRET

import os
import requests
import base64
from retrying import retry

# 获取环境变量
_EZCONFIG_ENV = os.getenv('EZCONFIG_ENV', 'DEV')
_EZCONFIG_APPID = os.getenv('EZCONFIG_APPID', '')
_EZCONFIG_SECRET = os.getenv('EZCONFIG_SECRET', '')
_EZCONFIG_HOST = os.getenv('EZCONFIG_HOST', 'http://localhost:8080')

# 获取最新配置的URL Path
_config_path = "/api/config/{APPID}/{ENV}"
# 获取配置最新版本号的URL Path
_config_version_path = "/api/version/{APPID}/{ENV}"

# 获取最新配置的URL
_config_url = _EZCONFIG_HOST + _config_path.format(APPID=_EZCONFIG_APPID, ENV=_EZCONFIG_ENV)
# 获取配置最新版本号的URL
config_version_url = _EZCONFIG_HOST + _config_version_path.format(APPID=_EZCONFIG_APPID, ENV=_EZCONFIG_ENV)
# Authorization header 值，注意值为base64编码
print("{0}:{1}".format(_EZCONFIG_APPID, _EZCONFIG_SECRET))
auth_token = "{0}:{1}".format(_EZCONFIG_APPID, _EZCONFIG_SECRET).encode('utf-8')
# 将auth_token转换为base64编码
auth_token = "Basic %s" % base64.b64encode(auth_token).decode('utf-8')


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def __parse_request():
    response = requests.get(_config_url, headers={'authorization': auth_token}, timeout=30)
    assert response.status_code == 200, "获取最新配置失败，错误码：{}".format(response.status_code)
    response_data = response.json()
    assert response_data['errno'] == 0, "获取最新配置失败，错误码：{}, 错误信息：".format(response_data['errno'], response_data['errmsg'])
    return response.json()["data"]


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def __parse_request_custom(auth_token: str, config_url: str):
    response = requests.get(config_url, headers={'authorization': auth_token}, timeout=30)
    assert response.status_code == 200, "获取最新配置失败，错误码：{}".format(response.status_code)
    response_data = response.json()
    assert response_data['errno'] == 0, "获取最新配置失败，错误码：{}, 错误信息：".format(response_data['errno'], response_data['errmsg'])
    return response.json()["data"]


# 从ezconfig获取配置
def get_latest_config() -> {"version": int, "config_data": dict, "config_hash": str}:
    """
    从ezconfig获取配置
    :return: {"version": int, "config_data": dict, "config_hash": str}
    """
    try:
        return __parse_request()
    except Exception as e:
        print(e)
        raise e


def get_latest_config_by_params(env: str, app_id: str, secret: str, host: str) -> {"version": int, "config_data": dict, "config_hash": str}:
    """
    传递环境参数，获取最新配置的方法
    :param env: str 环境参数 DEV or PRD
    :param app_id: str 应用ID
    :param secret: str 应用密钥
    :param host: str 配置中心地址 格式: http://localhost:8080
    :return: dict {"version": int, "config_data": dict, "config_hash": str}
    """
    config_path = "/api/config/{APPID}/{ENV}"
    # 获取最新配置的URL
    config_url = host + config_path.format(APPID=app_id, ENV=env)
    # Authorization header 值，注意值为base64编码
    print("{0}:{1}".format(app_id, secret))
    auth_token = "{0}:{1}".format(app_id, secret).encode('utf-8')
    # 将auth_token转换为base64编码
    auth_token = "Basic %s" % base64.b64encode(auth_token).decode('utf-8')

    try:
        return __parse_request_custom(auth_token, config_url)
    except Exception as e:
        print(e)
        raise e

