# coding: utf-8
# venv36
import sys
import readchar
from enum import Enum, auto
# 自作モジュール
import cv_camera
import playwave


class Phase(Enum):
    # auto()自動割当 開始indexは1
    NONE = auto()
    SELECT = auto()
    TAKE_A_IMAGE_OF_WAVE = auto()
    IMPORT_WAVE = auto()
    EXIT = auto()


# 初期フェーズはSELECT
PHASE = Phase.SELECT


# コマンド選択画面
def SCENE_SELECT():
    global PHASE
    print("-----------------------------------------------------------------")
    print(r" _   _ _       _                 _       _          _           |")
    print(r"| \ | (_)_ __ | |_ ___ _ __   __| | ___ | |    __ _| |__   ___  |")
    print(r"|  \| | | '_ \| __/ _ \ '_ \ / _` |/ _ \| |   / _` | '_ \ / _ \ |")
    print(r"| |\  | | | | | ||  __/ | | | (_| | (_) | |__| (_| | |_) | (_) ||")
    print(r"|_| \_|_|_| |_|\__\___|_| |_|\__,_|\___/|_____\__,_|_.__/ \___/ |")
    print("-----------------------------------------------------------------")
    print("NLaboを実行します")
    print("1.カメラで波形を取り込む")
    print("2.既存のファイルから波形を読み込む")
    print("Qキーで終了します")
    print("----------------------------------------------------------------")
    # キーボード入力受付 フェーズ切り替え
    kb = readchar.readchar()
    # print(kb)
    if kb == b"1":
        PHASE = Phase.TAKE_A_IMAGE_OF_WAVE
    elif kb == b"2":
        PHASE = Phase.IMPORT_WAVE
    elif kb == b"q":
        PHASE = Phase.EXIT
    print("PHASE " + PHASE.name + " に移行します")
    # コマンド実行
    SCENE_COMMAND()


# コマンド実行
def SCENE_COMMAND():
    global PHASE
    # カメラを起動
    if PHASE == Phase.TAKE_A_IMAGE_OF_WAVE:
        print("カメラを起動します")
        cv_camera.Enable_Camera()

        # 波形が保存されたら フェーズを切替
        if cv_camera.SAVED_FLAG:
            PHASE = Phase.IMPORT_WAVE
    # 波形を読み込む
    elif PHASE == Phase.IMPORT_WAVE:
        print("波形を読み込みます")
        playwave.PlayWave()
    # 終了
    elif PHASE == Phase.EXIT:
        print("終了します")
        sys.exit()


if __name__ == "__main__":
    while True:
        # コマンド選択画面
        SCENE_SELECT()
        # セレクト画面へ戻る
        PHASE = Phase.SELECT
