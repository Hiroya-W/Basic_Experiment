# coding: utf-8
# venv36

import cv2
import sys
from matplotlib import pyplot
import struct
# import numpy as np
# from scipy.interpolate import interp1d
# import math
import pyaudio


def main():
    # グレースケールでカラー画像を読み込む
    img = cv2.imread("./nlabo/data/TRIMEDIMGS/IMG_TRIM_2.png",
                     cv2.IMREAD_UNCHANGED)

    cv2.imshow("IMG", img)

    # 画像ファイルの読み込みに失敗したらエラー終了
    if img is None:
        print("Failed to load image file.")
        sys.exit(1)
    else:
        print("Success load image file.")
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
    # 検出結果
    # print(len(data))
    # [-32768, 32767]の整数値に変換
    # data = [int(x * 32767.0) for x in data]
    # pyplot.plot(data)
    # pyplot.show()

    # 音を鳴らす
    # data_wave = createWave(data, 440, 8000, 1)
    # play(data_wave, 8000 * 440, 16)

    # データを一時的に保管
    temp = data
    # 周波数f0の波形を作成
    for i in range(10):
        data.extend(temp)

    print("Create Wave")

    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
    pyplot.plot(data)
    pyplot.show()
    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される

    # ストリームを開く
    print("Play")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=int(128000), output=True)

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


# 周波数f0 サンプリング周波数fs 長さlengthの正弦波
def createWave(data, f0, fs, length):

    # データを一時的に保管
    temp = data
    # 周波数f0の波形を作成
    for i in range(10):
        data.extend(temp)

    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
    return data


"""
    time = math.floor(len(data) / fs)
    # サンプリングする
    data_new = []
    for i in range(fs):
        data_new.append(data[i * time])
    # グラフに描画
    pyplot.plot(data_new)
    pyplot.show()
"""
"""
    # サンプリング周波数を確保 補間で
    x = np.arange(len(data))
    # 3次スプライン補間
    f = interp1d(x, data, kind="cubic")
    # 必要な点数 0~len(data)までの間で6*f0個のデータを取得したい
    # xnew = np.linspace(0, len(data) - 1, num=6 * f0)
    xnew = np.linspace(0, len(data) - 1, num=fs)
    # サンプリングする
    data_new = f(xnew)
    # グラフに描画
    # pyplot.plot(xnew, data_new)
    # pyplot.show()
    # print(len(data_new))
    print("サンプリング完了" + str(len(data_new)))

    # [-32768, 32767]の整数値に変換
    data_new = [int(x * 32767.0) for x in data_new]
    # pyplot.plot(data)
    # pyplot.show()

    for i in range(fs * length):
        data_new.extend(data_new)

    # バイナリに変換
    data_new = struct.pack("h" * len(data_new),
                           *data_new)  # listに*をつけると引数展開される

    return data_new
"""


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


if __name__ == "__main__":
    main()
