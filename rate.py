"""
    利率计算
        - 等额本息
        - 等额本金
"""

import math

import numpy as np


def pay1(loans, rates, months):
    # 等额本息
    s = rates / 12
    I = s * math.pow(1 + s, months) / (math.pow(1 + s, months) - 1)
    monthly_payment = np.around(loans * I, 2)  # 计算每月应还款金额
    total_payment = np.around(monthly_payment * months, 2)  # 还款总额
    return monthly_payment, total_payment


def pay2(loans, rates, months):
    # 等额本金
    s = rates / 12
    monthly_payment = np.zeros(months)  # 初始化每月还款金额
    for i in range(0, months):
        monthly_payment[i] = np.around((loans / months) + ((loans - i * (loans / months)) * s), 2)  # 每月还款金额
    total_payment = np.around(sum(monthly_payment), 2)  # 计算还款总额
    return monthly_payment, total_payment


if __name__ == '__main__':
    total = 600000  # 总价
    first = total * 0.4  # 首付
    year = 20  # 贷款年限
    month = year * 12
    rate = [round(i * 0.001, 3) for i in range(15, 65)]
    for i in rate:
        t = round((total - first) * (1 + i * year), 2)
        # 等额本息
        p1 = pay1(total - first, i, month)
        # 等额本金
        p2 = pay2(total - first, i, month)
        print(
            f"总价{round(total / 10000)}w,"
            f"首付{round(first / 10000, 2)}w,"
            f"贷款{round((total - first) / 10000, 2)}w,"
            f"贷款{year}年,利率{round(i * 100, 1)}%\t"
            f"(等额本息) --> 还本付息{format(round(p1[1] / 10000, 2), '.2f')}w,"
            f"月供{format(p1[0], '.2f')} \t"
            f"(等额本金) --> 还本付息{format(round(p2[1] / 10000, 2), '.2f')}w,"
            f"月供(首){format(p2[0][0], '.2f')}(末){format(p2[0][-1], '.2f')}"
        )
