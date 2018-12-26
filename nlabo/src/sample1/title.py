# coding: utf-8
# venv36
import sys
# import readchar
from enum import Enum, auto
import pygame
from pygame.locals import QUIT
from pygame.locals import KEYDOWN
from pygame.locals import K_UP
from pygame.locals import K_DOWN
# from pygame.locals import K_SPACE
from pygame.locals import K_RETURN
from pygame.locals import K_ESCAPE
from pygame.locals import K_q

# 自作モジュール
import cv_camera
import playwave


# フェーズをENUMで管理
class Phase(Enum):
    # auto()自動割当 開始indexは1
    NONE = auto()
    SELECT = auto()
    TAKE_A_IMAGE_OF_WAVE = auto()
    IMPORT_WAVE = auto()
    EXIT = auto()


# 初期フェーズはSELECT
PHASE = Phase.SELECT


# NINTONDO LABO
def PRINT_LOGO():
    print("-----------------------------------------------------------------")
    print(r" _   _ _       _                  _       _          _           ")
    print(r"| \ | (_)_ __ | |_ ___  _ __   __| | ___ | |    __ _| |__   ___  ")
    print(r"|  \| | | '_ \| __/ _ \| '_ \ / _` |/ _ \| |   / _` | '_ \ / _ \ ")
    print(r"| |\  | | | | | || (_) | | | | (_| | (_) | |__| (_| | |_) | (_) |")
    print(r"|_| \_|_|_| |_|\__\___/|_| |_|\__,_|\___/|_____\__,_|_.__/ \___/ ")
    print("-----------------------------------------------------------------")
    print("NintondoLabo")


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


# コマンド選択画面
def SCENE_SELECT():
    # ロゴ表示
    PRINT_LOGO()
    # グローバル変数
    global PHASE

    # 画面サイズ
    SCREEN_SIZE = (640, 480)

    # Pygameの初期化
    pygame.init()
    # ウィンドウサイズの指定
    screen = pygame.display.set_mode(SCREEN_SIZE)
    # ウィンドウの名前の指定
    pygame.display.set_caption("Title Window")

    # フォントの作成
    # Noneでfreesansbold.ttfになる
    titlefont = pygame.font.Font("./nlabo/lib/fonts/NuKinakoMochiFwCt-Reg.otf",
                                 65)
    font = pygame.font.Font("./nlabo/lib/fonts/NuKinakoMochiFwCt-Reg.otf", 35)
    # テキストを描画したSurfaceを作成
    # 文字列 アンチエイリアシング 文字色 背景の色

    # str
    # タイトル
    t1str = "描いた波形の音を"
    t2str = "ならしてみよう"
    # 文字列を格納する配列
    liststr = [" 1.はけい　を　さつえい　する", " 2.はけい　を　よみこむ", " 3.とじる"]
    # 書式
    title1 = titlefont.render(t1str, True, (255, 255, 255))
    title2 = titlefont.render(t2str, True, (255, 255, 255))
    list_fmt = [
        font.render(">" + liststr[0], True, (255, 255, 255)),
        font.render(" " + liststr[1], True, (255, 255, 255)),
        font.render(" " + liststr[2], True, (255, 255, 255))
    ]
    # 実行中メッセージ
    mesfont = pygame.font.Font("./nlabo/lib/fonts/NuKinakoMochiFwCt-Reg.otf",
                               90)
    message = ["カメラ", "きどうちゅう"]
    mes_fmt = [
        mesfont.render(message[0], True, (255, 255, 255)),
        mesfont.render(message[1], True, (255, 255, 255))
    ]

    # 項目
    LIST_LENGTH = len(liststr)
    # 選択した番号
    SELECT_NUM = 1
    # 決定フラグ
    DETERMINED = False

    # 選択されるまでループ
    while DETERMINED is False:
        # カーソル 描画
        def set_list_format(NEXT_NUM):
            for i, s in enumerate(liststr):
                if i == NEXT_NUM - 1:
                    list_fmt[i] = font.render(">" + s, True, (255, 255, 255))
                else:
                    list_fmt[i] = font.render(" " + s, True, (255, 255, 255))

        # 画面を黒で塗りつぶし
        screen.fill((0, 0, 0))

        # テキスト描画
        screen.blit(title1, (40, 40))
        screen.blit(title2, (140, 120))
        screen.blit(list_fmt[0], (20, 300))
        screen.blit(list_fmt[1], (20, 350))
        screen.blit(list_fmt[2], (20, 400))
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
                sys.exit()
            # 選択
            if event.type == KEYDOWN and event.key == K_UP:
                NEXT_NUM = SELECT_NUM - 1
                # 範囲チェック
                if (1 <= NEXT_NUM):
                    SELECT_NUM = NEXT_NUM
                    print(str(NEXT_NUM))
                    set_list_format(NEXT_NUM)
                    # list1 = font.render(">" + l1str, True, (255, 255, 255))
                    # list2 = font.render(" " + l2str, True, (255, 255, 255))

            elif event.type == KEYDOWN and event.key == K_DOWN:
                NEXT_NUM = SELECT_NUM + 1
                # 範囲チェック
                if (NEXT_NUM <= LIST_LENGTH):
                    SELECT_NUM = NEXT_NUM
                    print(str(NEXT_NUM))
                    set_list_format(NEXT_NUM)
                    # list1 = font.render(" " + l1str, True, (255, 255, 255))
                    # list2 = font.render(">" + l2str, True, (255, 255, 255))

            # 決定
            elif event.type == KEYDOWN and event.key == K_RETURN:
                DETERMINED = True
                print("DETERMINED")
                break

    # 画面を黒で塗りつぶし
    screen.fill((0, 0, 0))
    # フェーズ切り替え
    if SELECT_NUM == 1:
        PHASE = Phase.TAKE_A_IMAGE_OF_WAVE
        screen.blit(mes_fmt[0], (185, 150))
        screen.blit(mes_fmt[1], (40, 240))
    elif SELECT_NUM == 2:
        PHASE = Phase.IMPORT_WAVE
    elif SELECT_NUM == 3:
        PHASE = Phase.EXIT
    # 画面更新
    pygame.display.update()

    print("PHASE " + PHASE.name + " に移行します")
    # コマンド実行
    SCENE_COMMAND()


if __name__ == "__main__":

    while True:
        # コマンド選択画面
        SCENE_SELECT()
        # セレクト画面へ戻る
        PHASE = Phase.SELECT
