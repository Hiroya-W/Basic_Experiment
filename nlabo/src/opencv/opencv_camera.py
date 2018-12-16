# coding: utf-8
# venv36
import cv2


def camera():

    # カメラのキャプチャを開始
    cam = cv2.VideoCapture(0)
    while True:
        # 画像を取得
        ret, img = cam.read()
        # ウィンドウに画像を表示
        cv2.imshow('PUSH ENTER KEY', img)
        # Enterキーが押されたら終了する
        if cv2.waitKey(1) == 13:
            break
    # 後始末
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camera()
