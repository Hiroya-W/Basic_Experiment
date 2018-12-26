# coding: utf-8
# venv36

import cv2
import sys
from matplotlib import pyplot
import numpy as np
import struct
import pyaudio
import os
import re
import copy


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

    # fft

    # 検出した波形を表示する
    # 2行1列のグラフの1番目の位置にプロット
    pyplot.subplot(211)
    pyplot.xlabel("time [sample]")
    pyplot.ylabel("amplitude")
    pyplot.plot(data)
    pyplot.pause(1)
    # pyplot.show()

    # データを一時的に保管
    temp = copy.deepcopy(data)
    # 再生時間
    length = 1.0
    freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
    FFT_FLAG = False
    for f in freqList:
        # 配列の中身を削除
        del data
        # 配列の中身を復元
        data = copy.deepcopy(temp)
        # サンプリング周波数を決定
        fs = width * f
        # 指定時間の長さ分の幅
        # points = fs * length
        copy_count = f * length
        # 取得した波形を複製して連結
        for i in range(int(copy_count)):
            data.extend(temp)
            # print(len(data))
        print("Created Wave")

        # このデータを使ってFFTする
        # 1回だけ
        # ドの音を用いてFFT
        if FFT_FLAG is False:
            FFT_FLAG = True
            start = 0  # サンプリングする開始位置
            N = 2048  # FFTのサンプル数
            hammingWindow = np.hamming(N)  # ハミング窓
            # 切り出した波形データに窓関数をかける
            windowedData = hammingWindow * data[start:start + N]
            windowedDFT = np.fft.fft(windowedData)
            fftfreqList = np.fft.fftfreq(N, d=1.0 / fs)
            windowedAmp = [np.sqrt(c.real**2 + c.imag**2) for c in windowedDFT]
            print("windowedAmp len: " + str(len(windowedAmp)))
            # 2行1列のグラフの2番目の位置にプロット
            pyplot.subplot(212)
            pyplot.plot(fftfreqList, windowedAmp, marker='o', linestyle='-')
            pyplot.axis([0, 5000, 0, 200])
            pyplot.xlabel("frequency [Hz]")
            pyplot.ylabel("amplitude spectrum")
            pyplot.pause(1)
            # pyplot.show()

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

    cv2.destroyAllWindows()
    pyplot.close()
