# coding: utf-8
# venv36

import cv2
# import numpy as np
from matplotlib import pyplot as plt


def camera():

    # カメラのキャプチャを開始
    cam = cv2.VideoCapture(0)
    while True:
        # 画像を取得
        ret, img = cam.read()
        # ウィンドウに画像を表示
        cv2.imshow('SAVE S KEY - EXIT ENTER KEY', img)

        if cv2.waitKey(1) & 0xFF == ord("s"):
            img_r = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR -> RGB順に
            plt.imshow(img_r, cmap='gray', interpolation='bicubic')
            # to hide tick values on X and Y axis
            plt.xticks([]), plt.yticks([])
            plt.show()

        # Enterキーが押されたら終了する
        if cv2.waitKey(1) == 13:
            break

    # 後始末
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camera()
