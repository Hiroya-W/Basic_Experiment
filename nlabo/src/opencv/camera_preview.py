# coding: utf-8
# venv36

import cv2

# import numpy as np
# from matplotlib import pyplot as plt

SAVED_FLAG = False
cam = None


def camera():

    # カメラのキャプチャを開始
    cam = cv2.VideoCapture(0)
    while True:
        # 画像を取得
        ret, img = cam.read()
        # ウィンドウに画像を表示
        cv2.imshow("SAVE S KEY - EXIT Q KEY", img)

        # キー入力用
        key = cv2.waitKey(1)

        # Sキーで画像を保存
        if key & 0xFF == ord("s"):
            print("SAVE")
            # コピーを作成
            img_saved = img
            # img_r = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR -> RGB順に
            # 表示
            cv2.imshow("SAVED IMG", img_saved)

        # Enterキーが押されたカメラを閉じる 13=Enter Key
        elif key == 13:
            if img_saved is not None:
                func_exit()
                break
            SAVED_FLAG = True

            # カメラをリリース
            cam.release()
            # カメラウィンドウを破棄
            cv2.destroyWindow("SAVE S KEY - EXIT Q KEY")
            print("CAMERA RELEASE")
            break

        # Qキーが押されたら終了する
        elif key & 0xFF == ord("q"):
            # 後処理
            func_exit()
            break

    # カメラを終了させるとき
    if SAVED_FLAG:
        show_savedimg()


def show_savedimg():
    while True:
        key = cv2.waitKey(1)
        # Qキーが押されたら終了する
        if key & 0xFF == ord("q"):
            func_exit()
            break


def func_exit():
    print("EXIT")
    # 後始末
    if cam is not None:
        cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camera()
