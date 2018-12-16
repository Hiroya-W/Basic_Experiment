# coding: utf-8
# venv36
# import os
# import wave
import struct
import numpy as np
import pyaudio
# import readchar
import sys
import pygame
from pygame.locals import *  # noqa

# import time
# from matplotlib import pyplot


def main():
    freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
    keyList = [K_s, K_d, K_f, K_g, K_h, K_j, K_k, K_l]  # noqa # SDFGHJKL

    (w, h) = (400, 400)  # 画面サイズ
    pygame.init()  # pygame初期化
    pygame.display.set_mode((w, h), 0, 32)  # 画面設定
    # screen = pygame.display.get_surface()

    while (1):
        f = 0  # 再生しない
        # pygame.display.update()  # 画面更新
        # pygame.time.wait(30)  # 更新時間間隔
        # screen.fill((0, 20, 0, 0))  # 画面の背景色

        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # キーに対して割り当てられた音を再生
        for i, key in enumerate(keyList):
            if pressed_keys[key]:
                f = freqList[i]

        if f != 0:
            print("周波数: ", f, "Hz")
            data = createSineWave(1.0, f, 8000.0, 1.0)
            play(data, 8000, 16)

        # イベント処理
        for event in pygame.event.get():
            # 画面の閉じるボタンを押したとき
            if event.type == QUIT:  # noqa
                print("QUIT")
                pygame.quit()
                sys.exit()
            # キーを押したとき
            if event.type == KEYDOWN:  # noqa
                # ESCキーなら終了
                if event.key == K_ESCAPE:  # noqa
                    print("QUIT")
                    pygame.quit()
                    sys.exit()


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
    # pyplot.plot(data[0, 100])
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
    main()
