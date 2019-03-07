#!/home/hiroya/Documents/Git-Repos/Basic_Experiment/.venv/bin/python
# -*- coding: utf-8 -*-

import cv2
import os
import nlbcfg as cfg

K_RETURN = 13
WINDOW_NAME_DISPLAY_VIDEO = "SAVE S KEY"
WINDOW_NAME_BINARY_IMAGE = "BINARY IMAGE"
WINDOW_NAME_TRIMMED_IMAGE = "SAVE & EXIT ENTER KEY - EXIT Q KEY"
shot_raw_image = None
trimmed_image = None


def main():
    """
    エントリポイント
    """
    startup_cam()


def extract_waveform_image():
    """
    波形部分の画像を抽出する
    """

    def get_binary_image():
        """
        撮影した画像から2値化画像を作成して返す
            :return binary_image: np.ndarray
                2値化画像変換後のデータ
        """
        image_removed_noise = cv2.medianBlur(shot_raw_image, 3)
        image_converted_gray = cv2.cvtColor(image_removed_noise, cv2.COLOR_BGR2GRAY)
        binary_image = cv2.adaptiveThreshold(
            image_converted_gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            9,
        )
        return binary_image

    def get_largest_outline():
        """
        一番大きな輪郭を取得して返す
            :return contours:
                検出できた中で一番大きな輪郭のデータ
        """
        area_list = []
        contours, hierarchy = cv2.findContours(
            binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE
        )
        for i in range(0, len(contours)):
            area = cv2.contourArea(contours[i])
            # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
            if area < 1e2 or 1e5 < area:
                area_list.append(0)
                continue
            area_list.append(area)

        max_value_index = area_list.index(max(area_list))
        return contours[max_value_index]

    def get_trimmed_image():
        """
        一番大きな輪郭でトリミングした2値化画像を返す
        検出できなかった場合はトリミングせずに返す
            :return binary_image: np.ndarray
                トリミング後のデータ
        """
        rect = get_largest_outline()
        if len(rect) > 0:
            x, y, w, h = cv2.boundingRect(rect)
            cv2.rectangle(shot_raw_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow(WINDOW_NAME_BINARY_IMAGE, binary_image)
            # トリミング
            # 少し内側をトリミングする
            offset = 0.06
            x += int(w * offset)
            y += int(h * offset)
            w -= 2 * int(w * offset)
            h -= 2 * int(h * offset)
            return binary_image[y : y + h, x : x + w]
        else:
            # 検出失敗した場合は元の画像を返す
            return binary_image

    global trimmed_image
    binary_image = get_binary_image()
    cv2.imshow(WINDOW_NAME_BINARY_IMAGE, binary_image)
    trimmed_image = get_trimmed_image()
    cv2.imshow(WINDOW_NAME_TRIMMED_IMAGE, trimmed_image)


def save_trimmed_image():
    """
    トリミングした画像を保存する
    """
    if trimmed_image is not None:
        file_index = 0
        file_Path = (
            cfg.SAVE_TARGET_PATH + cfg.SAVE_IMAGE_NAME + str(file_index) + ".png"
        )
        # ファイルの存在チェック
        while True:
            if os.path.exists(file_Path):
                file_index += 1
            else:
                break
            # ファイルが存在するならリネームして再チェック
            file_Path = (
                cfg.SAVE_TARGET_PATH + cfg.SAVE_IMAGE_NAME + str(file_index) + ".png"
            )
        # 保存
        cv2.imwrite(file_Path, trimmed_image)
        print(file_Path + "に保存しました")


def startup_cam():
    """
    カメラを起動する
    """

    def end_camera():
        """
        カメラを終了する
        """
        cam.release()
        cv2.destroyAllWindows()

    global shot_raw_image
    isEnd = False
    cam = cv2.VideoCapture(0)

    while not isEnd:
        # 映像の表示とキーイベント処理
        ret, img = cam.read()
        cv2.imshow(WINDOW_NAME_DISPLAY_VIDEO, img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            shot_raw_image = img
            extract_waveform_image()
        elif key == K_RETURN:
            save_trimmed_image()
            isEnd = True
        elif key == ord("q"):
            isEnd = True

    end_camera()


def get_cameras_count():
    """
    利用可能なカメラの数を数える
    https://stackoverrun.com/ja/q/1865684
    """
    max_tested = 10
    for i in range(max_tested):
        temp_camera = cv2.VideoCapture(i)
        if temp_camera.isOpened():
            temp_camera.release()
            continue
        return i


if __name__ == "__main__":
    main()
