import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ezconfig_client import loader


# from ezconfig_client import loader

# 通过环境变量配置进行获取
# res = loader.get_latest_config()

# 通过自定义透传参数获取
res = loader.get_latest_config_by_params("DEV", "xxx", "xxx", "https://xxxx.xxx.xxx")

print(res['version'])
print(res['config_data'])
print(res['config_hash'])
