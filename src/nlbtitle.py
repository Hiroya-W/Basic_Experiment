#!/home/hiroya/Documents/Git-Repos/Lets_Play_Your_Waveform/.venv/bin/python
# -*- coding: utf-8 -*-

import sys
from enum import Enum, auto
import pygame
from pygame.locals import QUIT
from pygame.locals import KEYDOWN
from pygame.locals import K_UP
from pygame.locals import K_DOWN
from pygame.locals import K_RETURN
from pygame.locals import K_ESCAPE
from pygame.locals import K_q

# 自作モジュール
import nlbcam
import nlbselection as slc
import nlbcfg as cfg


# フェーズをENUMで管理
class Phase(Enum):
    # auto()自動割当 開始indexは1
    NONE = auto()
    TITLE = auto()
    TAKE_WAVEFORM_IMAGE = auto()
    LOAD_WAVEFORM = auto()
    EXIT = auto()


# 初期フェーズはTITLE
phase = Phase.TITLE

# ウィンドウサイズの指定
DISPLAY_SIZE = (640, 480)
# ウィンドウの名前の指定
DISPLAY_CAPTION = "描いた波形の音をならしてみよう"
# fmt: off
# 描画テキスト
TITLE_TEXTS   = ["描いた波形の音を", "ならしてみよう"]
OPTION_TEXTS  = [" 1.はけい　を　さつえい　する", " 2.はけい　を　よみこむ", " 3.とじる"]
OPTION_LENGTH = len(OPTION_TEXTS)
CURSOR_TEXT   = ">"
SPACE_TEXT    = " "
# fmt: on


def main():
    """
    エントリポイント
    """
    # ロゴ表示
    print_logo()
    while True:
        scene_title()
        scene_command()


def print_logo():
    """
    NintondoLaboのAAを表示
    """
    print("-----------------------------------------------------------------")
    print(r" _   _ _       _                  _       _          _           ")
    print(r"| \ | (_)_ __ | |_ ___  _ __   __| | ___ | |    __ _| |__   ___  ")
    print(r"|  \| | | '_ \| __/ _ \| '_ \ / _` |/ _ \| |   / _` | '_ \ / _ \ ")
    print(r"| |\  | | | | | || (_) | | | | (_| | (_) | |__| (_| | |_) | (_) |")
    print(r"|_| \_|_|_| |_|\__\___/|_| |_|\__,_|\___/|_____\__,_|_.__/ \___/ ")
    print("-----------------------------------------------------------------")


def scene_command():
    """
    コマンド選択に対する画面遷移
    """
    global phase
    # カメラを起動
    if phase == Phase.TAKE_WAVEFORM_IMAGE:
        pygame.quit()
        nlbcam.startup_cam()
        # 波形が保存されたら フェーズを切替
        # if cv_camera.SAVED_FLAG:
        # phase = Phase.IMPORT_WAVE
        # scene_command()
    # 波形を読み込む
    elif phase == Phase.LOAD_WAVEFORM:
        pygame.quit()
        slc.main()
    # 終了
    elif phase == Phase.EXIT:
        sys.exit()


def scene_title():
    """
    タイトル画面の表示
    """

    def title_text_display():
        """
        タイトルとオプション一覧のテキスト表示
        """
        screen.fill(cfg.COLER_BLACK)
        # テキスト描画
        screen.blit(title_text_surfaces[0], (40, 40))
        screen.blit(title_text_surfaces[1], (140, 120))
        screen.blit(option_text_surfaces[0], (20, 300))
        screen.blit(option_text_surfaces[1], (20, 350))
        screen.blit(option_text_surfaces[2], (20, 400))

    def cursor_move(next_line_count):
        """
        カーソルを移動させる
            :param next_line_count: int
                次に移動する予定の行数
        """
        nonlocal current_line_number
        # カーソルが範囲内ならカーソル移動させる
        if 0 <= next_line_count <= OPTION_LENGTH - 1:
            current_line_number = next_line_count
            for i, surface in enumerate(option_text_surfaces):
                # 文字列の変更はsurfaceを変更する
                # fmt: off
                if i == current_line_number:
                    option_text_surfaces[i] = get_surface_added_cursor(
                        OPTION_TEXTS[i]
                    )
                else:
                    option_text_surfaces[i] = get_surface_deleted_cursor(
                        OPTION_TEXTS[i]
                    )
                # fmt: on

    def toggle_phase():
        """
        フェーズを切り替える
        """
        global phase
        if current_line_number == 0:
            phase = Phase.TAKE_WAVEFORM_IMAGE
        elif current_line_number == 1:
            phase = Phase.LOAD_WAVEFORM
        elif current_line_number == 2:
            phase = Phase.EXIT

    def input_event_handling():
        """
        入力イベントに対する処理
        """
        nonlocal hasDetermined
        global phase
        isEnd = False
        for event in pygame.event.get():
            # ウィンドウのxボタン
            isEnd = event.type == QUIT
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    isEnd = True
                elif event.key == K_UP:
                    cursor_move(current_line_number - 1)
                elif event.key == K_DOWN:
                    cursor_move(current_line_number + 1)
                elif event.key == K_RETURN:
                    hasDetermined = True
                    toggle_phase()

        if isEnd:
            hasDetermined = True
            phase = Phase.EXIT

    def get_surface_added_cursor(text):
        """
        textにカーソルを追加し作成したsurfaceを返す
            :param text: str
                追加する対象の文字列
        """
        return option_font.render(CURSOR_TEXT + text, True, cfg.COLER_BLUE)

    def get_surface_deleted_cursor(text):
        """
        textからカーソルを削除し作成したsurfaceを返す
            :param text: str
                削除する対象の文字列
        """
        return option_font.render(SPACE_TEXT + text, True, cfg.COLER_WHITE)

    global phase
    current_line_number = 0
    hasDetermined = False

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption(DISPLAY_CAPTION)
    # fmt: off
    # フォントの作成
    title_font   = pygame.font.Font(cfg.KINAKO_FONT_PATH, 65)
    option_font  = pygame.font.Font(cfg.KINAKO_FONT_PATH, 35)
    # fmt: on

    # フォントファイルからテキストを描画したsurfaceを作成
    title_text_surfaces = [
        title_font.render(TITLE_TEXTS[0], True, cfg.COLER_WHITE),
        title_font.render(TITLE_TEXTS[1], True, cfg.COLER_WHITE),
    ]
    option_text_surfaces = [
        # カーソルの初期位置にカーソル表示
        get_surface_added_cursor(OPTION_TEXTS[0]),
        get_surface_deleted_cursor(OPTION_TEXTS[1]),
        get_surface_deleted_cursor(OPTION_TEXTS[2]),
    ]

    # 決定するまでキー入力を受け付ける
    while not hasDetermined:
        title_text_display()
        input_event_handling()
        # 画面更新
        pygame.display.update()


if __name__ == "__main__":
    main()
