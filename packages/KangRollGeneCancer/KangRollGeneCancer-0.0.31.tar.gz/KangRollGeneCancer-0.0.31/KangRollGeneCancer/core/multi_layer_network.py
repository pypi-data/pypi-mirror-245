import numpy as np

def update_network(u, tau, B):
    """根据差分方程更新网络状态"""
    return u + tau * (B - u)

# 初始化参数
tau_1, B_1 = 0.1, 1
tau_2, B_2 = 0.1, 1
u_1, u_2 = 0, 0  # 初始状态

# 更新网络状态
for _ in range(10):  # 假设迭代10次
    u_1 = update_network(u_1, tau_1, B_1)
    u_2 = update_network(u_2, tau_2, B_2)

print("变异程度:", u_1, "修复程度:", u_2)
