# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot

# 振幅A 基本周波数f0 サンプリング周波数fs 長さ[秒]length


def createWave():
    # パラメータ
    a0 = 2 / np.pi
    length = 5
    fs = 1000

    # データ作成
    data = []
    for n in np.arange(length * fs):
        s = 0
        # 数式
        for k in range(1, 20):
            s += (-4) / (np.pi * (4 * k * k - 1))
            s *= np.cos(2 * np.pi * k * n / fs)
        s += a0
        data.append(s)
    pyplot.plot(data)
    pyplot.show()


if __name__ == "__main__":
    createWave()
