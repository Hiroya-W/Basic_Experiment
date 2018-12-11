# coding: utf-8
# venv
import sys
# import os
# import pyqtgraph as pg
# import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel


# ウィンドウ作成クラス
# QWidgetクラスを継承
class ExampleWidget(QWidget):
    # オブジェクト生成時に呼び出される関数
    # コンストラクタ
    # 関数の引数には self を書く javaでいうthisのような扱いで自分自身を呼び出せる
    def __init__(self):
        # superで継承元のinitを呼び出す
        super().__init__()
        # 初期化関数
        self.initUI()

    # 初期化関数
    def initUI(self):
        # ウィンドウサイズ
        self.resize(250, 150)
        # ウィンドウ位置
        self.move(300, 300)
        # ウィンドウタイトル
        self.setWindowTitle("sample")

        # buttonの設定
        self.button = QPushButton("Clear!!")
        self.label = QLabel("Connected")

        # buttonのclickでラベルをクリア
        self.button.clicked.connect(self.label.clear)

        # レイアウト配置
        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 0, 1, 1)
        self.grid.addWidget(self.label, 1, 0, 1, 2)
        self.setLayout(self.grid)

        # ウィンドウの表示
        self.show()


# 自分が実行されたときにだけ呼び出されるような書き方
if __name__ == "__main__":

    # appを宣言
    app = QApplication(sys.argv)
    # オブジェクトを作成
    ew = ExampleWidget()
    # 終了
    sys.exit(app.exec_())
