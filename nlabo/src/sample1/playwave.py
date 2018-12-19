# coding: utf-8
# venv36

import cv2
# import sys
# from matplotlib import pyplot
# import struct
import pyaudio
# import readchar
import os
import re


# キーボードから入力を受け付け
# 数字だったらそれを返す
def Keyin():
    # ファイル数を数える
    files = FilesCounter()
    print("読み込む画像の番号を入力してください")
    print(" 0~" + files + " ")
    while True:
        kb = input()
        # 数字なら
        if kb.isdigit():
            # 存在するファイル番号以内なら
            if 0 <= kb and kb <= files:
                break
            else:
                print("0~" + files + "の数字を入力してください")
        else:
            print("数字を入力してください")
    return kb


# ディレクトリに存在するファイル数を数える
def FilesCounter():
    dir = "./nlabo/data/TRIMEDIMGS/"
    files = os.listdir(dir)
    count = 0
    for file in files:
        # 拡張子はpngのみ
        index = re.search(".png", file)
        if index:
            count += 1
    return count


def PlayWave():
    # 読み込むファイルの番号を指定
    img_index = Keyin()

    # グレースケールでカラー画像を読み込む
    img = cv2.imread(
        "./nlabo/data/TRIMEDIMGS/IMG_TRIM_" + str(img_index) + ".png",
        cv2.IMREAD_UNCHANGED)

    cv2.imshow("IMG", img)


def play(data, fs, bit):
    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=int(fs), output=True)

    # チャンク単位でストリームに出力し音声を再生
    chunk = 1024
    sp = 0  # 再生位置ポインタ
    buffer = data[sp:sp + chunk]
    while buffer != b"":
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp:sp + chunk]
        # print(buffer)
    stream.close()
    p.terminate()


# if __name__ == "__main__":
# keyin()
