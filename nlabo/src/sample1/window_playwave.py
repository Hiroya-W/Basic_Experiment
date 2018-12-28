# coding: utf-8
# venv36
# import sys
import pygame
import os
import re
import cv2
import sys
import copy
import struct
import pyaudio
import numpy as np
from matplotlib import pyplot
from pygame.locals import QUIT
from pygame.locals import KEYDOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_RETURN
from pygame.locals import K_UP
from pygame.locals import K_DOWN
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_q
from pygame.locals import K_s, K_d, K_f, K_g, K_h, K_j, K_k, K_l



# ディレクトリに存在するファイル数を数える
def FilesDetector():
    dir = "./nlabo/data/TRIMEDIMGS/"
    files = []
    temps = os.listdir(dir)
    count = 0
    for file in temps:
        # 拡張子はpngのみ
        index = re.search(".png", file)
        if index:
            files.append(file)
            count += 1
    return count, files


def PlayWave():
    # 保存されているファイルを検出
    count, files = FilesDetector()
    # 画像を読み込む
    images = []
    dir = "./nlabo/data/TRIMEDIMGS/"

    for i in range(count):
        images.append(pygame.image.load(dir + "IMG_TRIM_" + str(i) + ".png"))


    # 画面サイズ
    SCREEN_SIZE = (1280, 1000)

    # Pygameの初期化
    pygame.init()
    # ウィンドウサイズの指定
    screen = pygame.display.set_mode(SCREEN_SIZE)
    # ウィンドウの名前の指定
    pygame.display.set_caption("Play Window")
    # フォントの作成
    font = pygame.font.Font("./nlabo/lib/fonts/NuKinakoMochiFwCt-Reg.otf", 35)
    filefont = pygame.font.Font("./nlabo/lib/fonts/NuKinakoMochiFwCt-Reg.otf",
                                15)
    # 文字列
    message = ["よみこむ　はけい　を　えらぶ : "]
    mes_fmt = [font.render(message[0], True, (255, 255, 255))]

    # 決定フラグ
    DETERMINED = False

    FINISH = False

    # ページ切り替え用
    PAGE = 0
    START = PAGE * 12
    # 選択位置
    CURSOR = START
    # 選択されるまでループ
    while DETERMINED is False:
        # 画面を黒で塗りつぶし
        screen.fill((0, 0, 0))
        # テキスト描画
        screen.blit(mes_fmt[0], (40, 40))

        # 画像を描画 3行4列で表示
        for i in np.arange(START, START + 12):
            # 範囲内なら
            if i < len(images):
                # ファイルの名前
                filename = "IMG_TRIM_" + str(i) + ".png"
                if CURSOR == i:
                    filename = "> " + filename
                    fmt = filefont.render(filename, True, (116, 169, 214))
                else:
                    fmt = filefont.render(filename, True, (255, 255, 255))

                # ファイル取得
                img = images[i]
                # 画像の解像度を取得して、リサイズする高さを計算
                resize_width = 270
                img_height = img.get_height()
                img_width = img.get_width()
                resize_height = int(resize_width / img_width * img_height)
                # 画像をリサイズ
                img = pygame.transform.scale(img,
                                             (resize_width, resize_height))
                col = int(i % 4)  # 列
                row = int(i / 4)  # 行
                row = row - PAGE * 3
                screen.blit(img, ((270 + 40) * col + 40,
                                  (270 + 40) * row + 100))

                # テキスト描画
                screen.blit(fmt, ((270 + 40) * col + 40,
                                  (270 + 60) * row + 310))

        # 画面更新
        pygame.display.update()
        # イベント処理
        for event in pygame.event.get():
            # 終了
            if event.type == QUIT or (event.type == KEYDOWN
                                      and event.key == K_ESCAPE) or (
                                          event.type == KEYDOWN
                                          and event.key == K_q):
                pygame.quit()

                FINISH = True

                DETERMINED = True
            # カーソル移動
            if event.type == KEYDOWN and event.key == K_UP:
                # 上に移動
                CURSOR -= 4
                print("K_UP")
            elif event.type == KEYDOWN and event.key == K_DOWN:
                # 下に移動
                CURSOR += 4
                print("K_DOWN")
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                # 右下角で右が入力されたとき
                if (CURSOR + 1) % 12 == 0:
                    # それより先に画像があったら
                    if CURSOR + 1 < len(images):
                        # ページ送り
                        PAGE += 1
                        START = PAGE * 12
                # 右に移動
                CURSOR += 1
                print("K_RIGHT")
            elif event.type == KEYDOWN and event.key == K_LEFT:
                # 左上角で左が入力されたとき
                if CURSOR % 12 == 0:
                    # ページが0じゃないとき
                    if PAGE is not 0:
                        # ページ戻り
                        PAGE -= 1
                        START = PAGE * 12
                # 左に移動
                CURSOR -= 1
                print("K_LEFT")
            # 決定
            elif event.type == KEYDOWN and event.key == K_RETURN:
                DETERMINED = True
                print("DETERMINED")
                # Windowを閉じる
                pygame.quit()
                break

            # カーソル位置調節
            # ページ0 左上角のとき
            if CURSOR < 0:
                # 0で止める
                CURSOR = 0
            # 右下角を超えたとき
            elif START + 11 < CURSOR:
                # 右下角に戻す
                CURSOR = START + 11
                # 画像がないところに行ったとき
                if len(images) - 1 < CURSOR:
                    # 画像があるところに戻す
                    CURSOR = len(images) - 1
            # 左上角を超えたとき
            elif CURSOR < START:
                # 左上角に戻す
                CURSOR = START
            # ページ内だけど画像がないところに行ったとき
            elif CURSOR < START + 11:
                # 画像があるところに戻す
                if len(images) - 1 < CURSOR:
                    CURSOR = len(images) - 1

            # print(str(CURSOR))


    if FINISH is False:
        # 読み込むファイルの番号を指定
        img_index = CURSOR
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
        # pyplot.pause(1)
        # pyplot.show(block=False)

        # データを一時的に保管
        temp = copy.deepcopy(data)
        # 再生時間
        length = 1.0
        freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
        keyList = [K_s, K_d, K_f, K_g, K_h, K_j, K_k, K_l]  # SDFGHJKL

        FFT_FLAG = False

        # 配列の中身を削除
        del data
        # 配列の中身を復元
        data = copy.deepcopy(temp)
        # サンプリング周波数を決定

        fs = width * freqList[0]
        # 指定時間の長さ分の幅
        # points = fs * length
        copy_count = freqList[0] * length

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

            # pyplot.show(block=False)

        # 画面サイズ
        SCREEN_SIZE = (525, 210)

        # Pygameの初期化
        pygame.init()
        # ウィンドウサイズの指定
        screen = pygame.display.set_mode(SCREEN_SIZE)
        # ウィンドウの名前の指定
        pygame.display.set_caption("KEY BOARD")

        while FINISH is False:
            f = 0  # 再生しない
            # 押されているキーをチェック
            pressed_keys = pygame.key.get_pressed()
            # キーに対して割り当てられた音を再生
            for i, key in enumerate(keyList):
                # KeyListに登録されたキーがあったら
                if pressed_keys[key]:
                    # その音に割り当てられた音を鳴らす
                    f = freqList[i]
                    # 白鍵盤を青くする
                    pygame.draw.rect(screen, (116, 169, 214),
                                     pygame.Rect((5 + 60) * i + 5, 5, 60, 200))
                else:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     pygame.Rect((5 + 60) * i + 5, 5, 60, 200))

            # 黒鍵盤
            for i in range(8):
                if i == 2 or i == 6:
                    continue
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect((5 + 60) * i + 35, 5, 60, 100))
            # 画面更新
            pygame.display.update()

            if f is not 0:
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

                # [-32768, 32767]の整数値に変換
                data = [int(x * 32767.0) for x in data]
                # pyplot.plot(data)
                # pyplot.show()
                # バイナリに変換
                data = struct.pack("h" * len(data),
                                   *data)  # listに*をつけると引数展開される

                # ストリームを開く
                print("Play")
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=int(fs),
                    output=True)

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

            # イベント処理
            for event in pygame.event.get():
                # 画面の閉じるボタンを押したとき
                # ESC,Qキーが押されたとき
                if event.type == QUIT or (event.type == KEYDOWN
                                          and event.key == K_ESCAPE) or (
                                              event.type == KEYDOWN
                                              and event.key == K_q):
                    print("Quit")
                    pygame.quit()
                    FINISH = True

        cv2.destroyAllWindows()
        pyplot.close()

