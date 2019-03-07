#!/home/hiroya/Documents/Git-Repos/Lets_Play_Your_Waveform/.venv/bin/python
# -*- coding: utf-8 -*-

import cv2
import sys
import struct
import pyaudio
import pygame
import numpy as np
from matplotlib import pyplot
import matplotlib.gridspec as gridspec
from pygame.locals import K_s, K_d, K_f, K_g, K_h, K_j, K_k, K_l
from pygame.locals import KEYDOWN
from pygame.locals import K_ESCAPE
from pygame.locals import QUIT
from pygame.locals import K_q


import nlbcfg as cfg


DISPLAY_SIZE = (525, 410)
DISPNAY_CAPTION = "KEY BOARD"
WINDOW_NAME_LOADED_IMAGE = "LOADED IMAGE"


# 再生時間
PLAY_LENGTH = 1.0
# ドレミファソラシド
FREQUENCY_LIST = [262, 294, 330, 349, 392, 440, 494, 523]
# SDFGHJKL
KEY_LIST = [K_s, K_d, K_f, K_g, K_h, K_j, K_k, K_l]


def main():
    """
    エントリポイント
    """
    SELECTED_IMAGE_COUNT = 1
    startup_player(SELECTED_IMAGE_COUNT)


def startup_player(SELECTED_IMAGE_COUNT):
    """
    音声を再生するためのプレイヤーを立ち上げる
        :param SELECTED_IMAGE_COUNT: int
            プレイヤーに読み込ませる画像の番号
            ex) IMG_TRIM_10.png --> SELECTED_IMAGE_COUNT = 10
    """

    def load_image():
        """
        画像を読み込む
            :return loaded_image: np.ndarray
                読み込んだ画像データ
        """
        loaded_image = cv2.imread(
            cfg.SAVE_TARGET_PATH
            + cfg.SAVE_IMAGE_NAME
            + str(SELECTED_IMAGE_COUNT)
            + ".png",
            cv2.IMREAD_UNCHANGED,
        )

        # 画像ファイルの読み込みに失敗したらエラー終了
        if loaded_image is None:
            print("Failed to load image file.")
            sys.exit(1)
        else:
            print("Success load image file.")

        return loaded_image

    def detect_waveform():
        """
        読み込んだ画像から波形データを作成する
            :return waveform_data: list
                作成した波形データ
        """
        waveform_data = []
        for col in range(LOADED_IMAGE_WIDTH - 1):
            one_column_data = loaded_image[:, col]
            index_having_zero_data = np.where(one_column_data == 0)
            # 0のインデックスがなかったとき
            if index_having_zero_data[0].size == 0:
                waveform_data.append(0)
            else:
                # 一番最初に見つかったデータだけ利用する
                value = index_having_zero_data[0].item(0)
                # 最大値 1 最小値 -1 に正規化
                normalized_data = 2 * value / LOADED_IMAGE_HEIGHT - 1
                # 範囲外になってしまうときは調整
                if normalized_data > 1.0:
                    normalized_data = 1.0
                elif normalized_data < -1.0:
                    normalized_data = -1.0

                data_inverted_up_and_down = normalized_data * -1
                waveform_data.append(data_inverted_up_and_down)

        return waveform_data

    def calculate_fft(waveform_data, fs):
        """
        docstring here
            :param waveform_data: list
                FFTの計算に用いるデータ
            :param fs: int
                FFTの計算に用いるサンプリング周波数

            :return fft_freq_list: np.array
                FFTの計算で得た周波数のリスト 横軸
            :return window_amp: np.array
                FFTの計算で得た振幅のリスト　縦軸

        """
        # サンプリングする開始位置
        SAMPLING_START_INDEX = 0
        N_USE_IN_FFT = 2048
        hamming_window = np.hamming(N_USE_IN_FFT)  # ハミング窓
        # 切り出した波形データに窓関数をかける
        windowed_data = (
            hamming_window
            * waveform_data[SAMPLING_START_INDEX : SAMPLING_START_INDEX + N_USE_IN_FFT]
        )
        windowed_dft = np.fft.fft(windowed_data)
        fft_freq_list = np.fft.fftfreq(N_USE_IN_FFT, d=1.0 / fs)
        windowed_amp = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in windowed_dft]

        return fft_freq_list, windowed_amp

    def show_waveform_information():
        """
        読み込んだ画像データ
        作成した波形データ
        FFTの計算結果
        を表示する
        """
        pyplot.figure(figsize=(10, 8))
        grid_spec = gridspec.GridSpec(2, 2)
        plt_loaded_image = pyplot.subplot(grid_spec[0, :])
        plt_waveform = pyplot.subplot(grid_spec[1, 0])
        plt_fft = pyplot.subplot(grid_spec[1, 1])

        plt_loaded_image.set_title("LOADED IMAGE")
        plt_loaded_image.imshow(loaded_image, pyplot.cm.gray)

        plt_waveform.set_title("WAVEFORM_DATA")
        plt_waveform.plot(waveform_data)
        plt_waveform.set_xlabel("time [sample]")
        plt_waveform.set_ylabel("amplitude")

        plt_fft.set_title("FFT_RESULT")
        plt_fft.plot(fft_freq_list, windowed_amp, linestyle="-")
        plt_fft.set_xlim(0, 5000)
        plt_fft.set_ylim(0, 200)
        plt_fft.set_xlabel("frequency [Hz]")
        plt_fft.set_ylabel("amplitude spectrum")
        pyplot.pause(1)

    def get_index_input_key():
        """
        入力されたキーが登録されているリストのどこにあるか調べて返す

            :return i: int
                リストのインデックス
                見つからなかったら-1を返す
        """
        pygame.event.pump()
        pressed_keys = pygame.key.get_pressed()
        for i, key in enumerate(KEY_LIST):
            if pressed_keys[key]:
                return i
        # キー入力がなかったら-1を返す
        return -1

    def input_event_handling():
        """
        ウィンドウのxボタン、Q、ESCキーの入力を処理
        どれも入力があれば終了フラグを立てる
        """
        nonlocal isEnd
        for event in pygame.event.get():
            # ウィンドウのxボタン
            isEnd = event.type == QUIT
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    isEnd = True

    def highlight_input_keyboard(index):
        """
        受け取ったインデックスに対応する鍵盤を青色表示する
            :param index: 押されたキーのインデックス
        """
        KEY_WIDTH = 60
        KEY_HEIGHT = 200
        KEY_OFFSET = 5
        for i, key in enumerate(KEY_LIST):
            if index == i:
                # 白鍵盤を青くする
                pygame.draw.rect(
                    screen,
                    cfg.COLER_BLUE,
                    pygame.Rect(
                        (KEY_OFFSET + KEY_WIDTH) * i + KEY_OFFSET,
                        KEY_OFFSET,
                        KEY_WIDTH,
                        KEY_HEIGHT,
                    ),
                )
            else:
                pygame.draw.rect(
                    screen,
                    cfg.COLER_WHITE,
                    pygame.Rect(
                        (KEY_OFFSET + KEY_WIDTH) * i + KEY_OFFSET,
                        KEY_OFFSET,
                        KEY_WIDTH,
                        KEY_HEIGHT,
                    ),
                )

        # 黒鍵盤
        for i in range(8):
            # 表示しない位置
            if i == 2 or i == 6:
                continue
            pygame.draw.rect(
                screen,
                cfg.COLER_BLACK,
                pygame.Rect(
                    (KEY_OFFSET + KEY_WIDTH) * i + KEY_OFFSET + KEY_WIDTH / 2,
                    KEY_OFFSET,
                    KEY_WIDTH,
                    KEY_HEIGHT / 2,
                ),
            )

        # 画面更新
        pygame.display.update()

    def play_waveform(original_waveform_data, FREQUENCY):
        """
        波形データを指定された周波数で再生する
            :param original_waveform_data: 再生する波形データ
            :param FREQUENCY: 再生する周波数
        """
        waveform_data_for_calculation = []
        SAMPLING_FREQUENCY = LOADED_IMAGE_WIDTH * FREQUENCY
        COPYING_TIMES = FREQUENCY * PLAY_LENGTH
        for i in range(int(COPYING_TIMES)):
            waveform_data_for_calculation.extend(original_waveform_data)
        waveform_data_for_calculation = [
            int(x * 32767.0) for x in waveform_data_for_calculation
        ]
        audio_data = struct.pack(
            "h" * len(waveform_data_for_calculation), *waveform_data_for_calculation
        )

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=int(SAMPLING_FREQUENCY),
            output=True,
        )

        # チャンク単位でストリームに出力し音声を再生
        chunk = 1024
        start_pointer = 0  # 再生位置ポインタ
        buffer = audio_data[start_pointer : start_pointer + chunk]
        while buffer != b"":
            stream.write(buffer)
            start_pointer = start_pointer + chunk
            buffer = audio_data[start_pointer : start_pointer + chunk]
        stream.close()
        p.terminate()

    isEnd = False
    # 2回連続で再生されるのを防ぐ
    previous_key_input_index = -1
    loaded_image = load_image()
    LOADED_IMAGE_HEIGHT, LOADED_IMAGE_WIDTH = loaded_image.shape[:2]
    waveform_data = detect_waveform()
    # その波形を500HzとしてFFTを計算
    # sampling_frequency == width なら1Hz
    SAMPLING_FREQUENCY = LOADED_IMAGE_WIDTH * 500
    COPYING_TIMES = SAMPLING_FREQUENCY * PLAY_LENGTH
    waveform_data_for_calculation = []
    for i in range(int(COPYING_TIMES)):
        waveform_data_for_calculation.extend(waveform_data)

    fft_freq_list, windowed_amp = calculate_fft(
        waveform_data_for_calculation, SAMPLING_FREQUENCY
    )

    show_waveform_information()

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption(DISPNAY_CAPTION)

    while not isEnd:
        index_input_key = get_index_input_key()
        input_event_handling()
        highlight_input_keyboard(index_input_key)
        # キー入力がなければ再生はしない
        if index_input_key == -1 or previous_key_input_index == index_input_key:
            previous_key_input_index = index_input_key
            continue

        previous_key_input_index = index_input_key
        PLAY_FREQUENCY = FREQUENCY_LIST[index_input_key]
        play_waveform(waveform_data, PLAY_FREQUENCY)

    pygame.quit()
    pyplot.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
