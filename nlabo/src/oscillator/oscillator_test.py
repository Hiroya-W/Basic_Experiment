# coding: utf-8
# venv36
# import os
# import wave
import struct
import numpy as np
import pyaudio
from matplotlib import pyplot


# 振幅A 基本周波数f0 サンプリング周波数fs 長さ[秒]length
# の正弦波を作成して返す
def createSineWave(A, f0, fs, length):
    data = []
    # [-1.0, 1.0]の小数値が入った波を作成
    for n in np.arange(length * fs):
        s = A * np.sin(2 * np.pi * f0 * n / fs)
        # 振幅が大きいときはクリッピング
        if s > 1.0:
            s = 1.0
        if s < -1.0:
            s = -1.0
        data.append(s)
    # [-32768, 32767]の整数値に変換
    data = [int(x * 32767.0) for x in data]
    # print(len(data))
    # pyplot.plot(data[0:100])
    # pyplot.show()

    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
    return data


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

    freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
    for f in freqList:
        print("周波数: ", f, "Hz")
        data = createSineWave(1.0, f, 8000.0, 1.0)
        play(data, 8000, 16)
