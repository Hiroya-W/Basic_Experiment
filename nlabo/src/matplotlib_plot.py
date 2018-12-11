# coding: utf-8
# venv36
import math
import numpy as np
from matplotlib import pyplot

# mathモジュールのπを利用
pi = math.pi

# 0から2πまでの範囲を100分割したnumpy配列
x = np.linspace(0, 2 * pi, 100)
sin_y = np.sin(x)
cos_y = np.cos(x)

# numpy配列やリストを引数として渡す
# 判例のためにlabelキーワードで凡例名をつける
pyplot.plot(x, sin_y, label="sin")
pyplot.plot(x, cos_y, label="cos")

# グラフタイトル
pyplot.title("Sin And Cos Graph")

# グラフの軸
pyplot.xlabel("X-Axis")
pyplot.ylabel("Y-Axis")

# グラフの凡例
pyplot.legend()

pyplot.show()
