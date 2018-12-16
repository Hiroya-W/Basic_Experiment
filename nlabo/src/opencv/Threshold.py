# coding: utf-8
# venv36

import cv2
import os
# import numpy as np
# from matplotlib import pyplot as plt

SAVED_FLAG = False
cam = None
img_tri = None


def camera():
    # グローバル変数とする
    global SAVED_FLAG
    global cam
    global img_tri

    # カメラのキャプチャを開始
    cam = cv2.VideoCapture(0)
    # print("カメラ　デフォルト設定")
    # print(cam.get(cv2.CAP_PROP_FPS))
    # print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    # print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #
    # cam.set(cv2.CAP_PROP_FPS, 60)  # カメラFPSを60FPSに設定
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定
    # print("カメラ　設定変更")
    # print(cam.get(cv2.CAP_PROP_FPS))
    # print(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    # print(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

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
            img_blur = cv2.medianBlur(img, 7)
            img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

            th3 = cv2.adaptiveThreshold(img_gray, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)

            # 輪郭を抽出
            #   contours : [領域][Point No][0][x=0, y=1]
            #   cv2.CHAIN_APPROX_NONE: 中間点も保持する
            #   cv2.CHAIN_APPROX_SIMPLE: 中間点は保持しない
            ret, contours, hierarchy = cv2.findContours(
                th3, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            # 矩形検出された数（デフォルトで0を指定）
            # detect_count = 0

            max_index = 0
            max_area = 0
            # 各輪郭に対する処理
            for i in range(0, len(contours)):

                # 輪郭の領域を計算
                area = cv2.contourArea(contours[i])

                # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
                if area < 1e2 or 1e5 < area:
                    continue

                # 一番大きい面積を調べる
                if max_area < area:
                    max_index = i
                    max_area = area

            # 外接矩形
            if len(contours[max_index]) > 0:
                rect = contours[max_index]
                x, y, w, h = cv2.boundingRect(rect)
                cv2.rectangle(img_saved, (x, y), (x + w, y + h), (0, 255, 0),
                              2)
                # トリミング
                img_tri = th3[y:y + h, x:x + w]
                # 表示
                cv2.imshow("SAVED IMG", img_tri)

            # img_r = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR -> RGB順に

        # Enterキーが押されたカメラを閉じる 13=Enter Key
        elif key == 13:
            if img_saved is not None:
                SAVED_FLAG = True

            # 保存
            file_index = 0
            file_Path = "./nlabo/data/TRIMEDIMGS/IMG_TRIM_" + str(
                file_index) + ".png"

            while True:
                if os.path.exists(file_Path):
                    print(file_Path + "は存在します")
                    file_index += 1
                else:
                    print(file_Path + "は存在しません")
                    break
                file_Path = "./nlabo/data/TRIMEDIMGS/IMG_TRIM_" + str(
                    file_index) + ".png"

            cv2.imwrite(file_Path, img_tri)
            print(file_Path + "に保存しました")

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


# カメラを終了して
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
