# coding: utf-8
# venv36

import cv2
import sys
from matplotlib import pyplot
import struct
import pyaudio
import os
import re


# キーボードから入力を受け付け
# 数字だったらそれを返す
def Keyin():
    # ファイル数を数える
    files = FilesCounter()
    print("読み込む画像の番号を入力してください")
    print(" 0~" + str(files - 1) + " ")
    while True:
        kb = input()
        # 数字なら
        if kb.isdigit():
            # 存在するファイル番号以内なら
            if 0 <= int(kb) and int(kb) <= files - 1:
                break
            else:
                print("0~" + str(files - 1) + "の数字を入力してください")
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

    # 画像ファイルの読み込みに失敗したらエラー終了
    if img is None:
        print("Failed to load image file.")
        sys.exit(1)
    else:
        print("Success load image file.")

    cv2.imshow("IMG", img)
    # カラーとグレースケールで場合分け
    if len(img.shape) == 3:
        height, width, channels = img.shape[:3]
    else:
        height, width = img.shape[:2]
        channels = 1

    # 取得結果（幅，高さ，チャンネル数，depth）を表示
    print("width: " + str(width))
    print("height: " + str(height))
    print("channels: " + str(channels))
    print("dtype: " + str(img.dtype))

    # 波形検出
    # 各1列で一番最初に見つけた黒を取り出す
    data = []
    for i in range(width - 1):
        for j in range(height - 1):
            # print(i, j)
            if (img.item(j, i) == 0):
                value = j
                value -= height / 2
                value *= -1
                value /= height

                if value > 1.0:
                    value = 1.0
                if value < -1.0:
                    value = -1.0
                data.append(value)
                break

    print("Finish Wave Detect")
    # 検出した波形を表示する
    pyplot.plot(data)
    pyplot.show()

    # データを一時的に保管
    temp = data
    # 取得した波形を複製して連結
    for i in range(10):
        data.extend(temp)
    print("Created Wave")

    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
    # pyplot.plot(data)
    # pyplot.show()
    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される

    # ストリームを開く
    print("Play")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=int(96000), output=True)

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
