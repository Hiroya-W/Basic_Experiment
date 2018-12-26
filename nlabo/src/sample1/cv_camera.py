# coding: utf-8
# venv36

import cv2
import os

SAVED_FLAG = False
cam = None
img_tri = None


def Enable_Camera():
    # グローバル変数とする
    global SAVED_FLAG
    global cam
    global img_tri

    # カメラのキャプチャを開始
    cam = cv2.VideoCapture(0)
    img_saved = None
    while True:
        # 画像を取得
        ret, img = cam.read()
        # ウィンドウに画像を表示
        cv2.imshow("SAVE S KEY", img)
        # ウィンドウ作成
        cv2.namedWindow("SAVE & EXIT ENTER KEY - EXIT Q KEY",
                        cv2.WINDOW_AUTOSIZE)
        # キー入力用
        key = cv2.waitKey(1)

        # Sキーで画像を保存
        if key & 0xFF == ord("s"):
            print("SAVE")
            # コピーを作成
            img_saved = img
            # ノイズ除去
            img_blur = cv2.medianBlur(img, 7)
            # グレー変換
            img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
            # 2値化
            th3 = cv2.adaptiveThreshold(img_gray, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)

            # 輪郭を抽出
            ret, contours, hierarchy = cv2.findContours(
                th3, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

            # 一番大きい輪郭を取り出す
            max_index = 0
            max_area = 0
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
                cv2.imshow("SAVE & EXIT ENTER KEY - EXIT Q KEY", img_tri)

        # Enterキーが押されたカメラを閉じる 13=Enter Key
        elif key == 13:
            # 写真を撮ってエンターキーが押されたとき
            if img_saved is not None:
                SAVED_FLAG = True
            else:
                # 後処理
                func_exit()
                break
            # 保存先の指定
            file_index = 0
            file_Path = "./nlabo/data/TRIMEDIMGS/IMG_TRIM_" + str(
                file_index) + ".png"
            # ファイルの存在チェック
            while True:
                if os.path.exists(file_Path):
                    print(file_Path + "は存在します")
                    file_index += 1
                else:
                    print(file_Path + "は存在しません")
                    break
                # リネームして再チェック
                file_Path = "./nlabo/data/TRIMEDIMGS/IMG_TRIM_" + str(
                    file_index) + ".png"
            # 保存
            cv2.imwrite(file_Path, img_tri)
            print(file_Path + "に保存しました")
            # 終了する
            # 後処理
            func_exit()
            break

        # Qキーが押されたら終了する
        elif key & 0xFF == ord("q"):
            # 後処理
            func_exit()
            break


def func_exit():
    print("EXIT")
    # 後始末
    if cam is not None:
        cam.release()
    cv2.destroyAllWindows()
