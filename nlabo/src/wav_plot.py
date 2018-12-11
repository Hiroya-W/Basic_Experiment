# coding: utf-8
# venv36
import os
import wave
import numpy as np
from matplotlib import pyplot


def printWaveInfo(wf):
    print("WAVEファイルの情報を取得")
    print("チャンネル数:", wf.getnchannels())
    print("サンプル幅:", wf.getsampwidth())
    print("サンプリング周波数:", wf.getframerate())
    print("フレーム数:", wf.getnframes())
    print("パラメータ:", wf.getparams())
    print("長さ(秒)", float(wf.getnframes()) / wf.getframerate())


if __name__ == "__main__":
    # 実行ファイルのパス
    base = os.path.dirname(os.path.abspath(__file__))
    # 実行ファイルのパスから相対的にファイルのパスを指定する
    wavpath = os.path.normpath(os.path.join(base, '../lib/wav/aqua.wav'))

    wf = wave.open(wavpath, "r")

    printWaveInfo(wf)

    buffer = wf.readframes(wf.getnframes())
    print(len(buffer))  # バイト数 = 1フレーム2バイト * フレーム数

    # bufferはバイナリなので2バイトずつ整数 (-32768から32767) にまとめる
    data = np.frombuffer(buffer, dtype="int16")

    # プロット
    # pyplot.plot(data)
    # データの一部のみをプロットする
    pyplot.plot(data[50000:50500])
    pyplot.show()
