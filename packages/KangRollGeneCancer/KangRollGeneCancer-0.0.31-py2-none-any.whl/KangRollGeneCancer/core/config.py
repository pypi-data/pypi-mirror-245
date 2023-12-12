# config.py

import os

IS_KANGROLL_PRODUCTION = os.getenv("IS_KANGROLL_PRODUCTION", "False") == "True"
KANGROLL_PRODUCTION_KEY = os.getenv("KANGROLL_PRODUCTION_KEY")

# 其他配置...



# # 设置为 True 时，表示在生产环境
# IS_PRODUCTION = True
# #False
# #True #

# # 生产环境密钥
# PRODUCTION_KEY = "KangRoll2023_key"

