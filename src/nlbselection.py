#!/home/hiroya/Documents/Git-Repos/Lets_Play_Your_Waveform/.venv/bin/python
# -*- coding: utf-8 -*-

import pygame
import os
import re
import numpy as np
from enum import Enum, auto
from pygame.locals import QUIT
from pygame.locals import KEYDOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_RETURN
from pygame.locals import K_UP
from pygame.locals import K_DOWN
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_q

import nlbcfg as cfg
import nlbplayer


# フェーズをENUMで管理
class Phase(Enum):
    # auto()自動割当 開始indexは1
    NONE = auto()
    SELECTION = auto()
    PLAY = auto()
    EXIT = auto()


# 初期フェーズはTITLE
phase = Phase.SELECTION

DISPLAY_SIZE = (1280, 1000)
DISPLAY_CAPTION = "読み込む波形を選ぶ"
MESSAGE_TEXT = "よみこむ　はけい　を　えらぶ : "
CURSOR_TEXT = "> "
SPACE_TEXT = " "

selected_image_count = 0


def main():
    """
    エントリポイント
    """
    while True:
        waveform_selection()

        if phase == Phase.EXIT:
            break

        nlbplayer.startup_player(selected_image)


def get_waveform_images():
    """
    ディレクトリに存在する画像を取得する
        :return loaded_image: pygame.image
            pygameで扱える用に読み込み、返す
    """
    images_name = []
    temps = os.listdir(cfg.SAVE_TARGET_PATH)
    count = 0
    for file in temps:
        # 拡張子はpngのみ
        index = re.search(".png", file)
        if index:
            images_name.append(file)
            count += 1

    loaded_images = []
    for i in range(count):
        loaded_images.append(
            pygame.image.load(
                cfg.SAVE_TARGET_PATH + cfg.SAVE_IMAGE_NAME + str(i) + ".png"
            )
        )

    return loaded_images


def waveform_selection():
    """
    読み込む波形を選択する
    """

    def get_surface_added_cursor(text):
        """
        textにカーソルを追加し作成したsurfaceを返す
            :param text: str
                追加する対象の文字列
            :return surface
                カーソル文字を追加、青色にしたテキストを書いたsurface
        """
        return filename_font.render(CURSOR_TEXT + text, True, cfg.COLER_BLUE)

    def get_surface_deleted_cursor(text):
        """
        textからカーソルを削除し作成したsurfaceを返す
            :param text: str
                削除する対象の文字列
            :return surface
                空白文字を追加、白色のテキストを書いたsurface
        """
        return filename_font.render(SPACE_TEXT + text, True, cfg.COLER_WHITE)

    def show_image():
        """
        画像を並べて表示する
        """
        for i in np.arange(start_index, start_index + IMAGE_COUNT_EACH_PAGE):
            # 画像が存在する枚数以内なら
            if i < len(loaded_images):
                filename = cfg.SAVE_IMAGE_NAME + str(i) + ".png"
                # カーソルがある位置ならファイル名にカーソルを追加
                if current_cursor_count == i:
                    filename_surface = get_surface_added_cursor(filename)
                else:
                    filename_surface = get_surface_deleted_cursor(filename)

                # ファイル取得
                img = loaded_images[i]
                # 画像の解像度を取得して、リサイズする高さを計算
                RESIZE_WIDTH = 270
                IMG_HEIGHT = img.get_height()
                IMG_WIDTH = img.get_width()
                RESIZE_HEIGHT = int(RESIZE_WIDTH / IMG_WIDTH * IMG_HEIGHT)
                # 画像をリサイズ
                img = pygame.transform.scale(img, (RESIZE_WIDTH, RESIZE_HEIGHT))
                # iから行,列の位置を計算
                COL = int(i % 4)  # 列
                ROW = int(i / 4)  # 行
                ROW = ROW - page_count * 3
                # 画像描画
                screen.blit(
                    img,
                    ((RESIZE_WIDTH + 40) * COL + 40, (RESIZE_WIDTH + 40) * ROW + 100),
                )

                # テキスト描画
                screen.blit(
                    filename_surface,
                    ((RESIZE_WIDTH + 40) * COL + 40, (RESIZE_WIDTH + 60) * ROW + 310),
                )

    def input_event_handling():
        """
        入力イベントに対する処理
        """
        nonlocal hasDetermined, current_cursor_count, page_count, start_index
        global phase, selected_image
        isEnd = False
        for event in pygame.event.get():
            # ウィンドウのxボタン
            isEnd = event.type == QUIT
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    isEnd = True
                elif event.key == K_UP:
                    current_cursor_count -= 4
                elif event.key == K_DOWN:
                    current_cursor_count += 4
                elif event.key == K_RIGHT:
                    # 右下で入力があったとき
                    if (current_cursor_count + 1) % 12 == 0:
                        # それより先に画像があったら
                        if current_cursor_count + 1 < len(loaded_images):
                            # ページ送り
                            page_count += 1
                            start_index = page_count * IMAGE_COUNT_EACH_PAGE
                    current_cursor_count += 1
                elif event.key == K_LEFT:
                    # 左上で入力があったとき
                    if current_cursor_count % 12 == 0:
                        if page_count != 0:
                            # ページ戻り
                            page_count -= 1
                            start_index = page_count * IMAGE_COUNT_EACH_PAGE
                    current_cursor_count -= 1
                elif event.key == K_RETURN:
                    hasDetermined = True
                    selected_image = current_cursor_count
                    phase = Phase.PLAY

                # カーソル位置の調整
                # 画像が存在しない範囲なら
                if current_cursor_count < 0:
                    current_cursor_count = 0
                # ページの範囲外なら
                elif current_cursor_count < start_index:
                    current_cursor_count = start_index
                # ページの範囲外なら
                elif start_index + 11 < current_cursor_count:
                    current_cursor_count = start_index + 11
                # 画像がないところなら
                elif len(loaded_images) - 1 < current_cursor_count:
                    current_cursor_count = len(loaded_images) - 1

        if isEnd:
            hasDetermined = True
            phase = Phase.EXIT

    # ページ切り替え用
    # 1ページには12枚の画像を表示
    page_count = 0
    IMAGE_COUNT_EACH_PAGE = 12
    start_index = page_count * IMAGE_COUNT_EACH_PAGE
    current_cursor_count = start_index

    hasDetermined = False

    # 保存されている波形画像をすべて読み込む
    loaded_images = get_waveform_images()

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption(DISPLAY_CAPTION)
    # fmt: off
    # フォントの作成
    message_font   = pygame.font.Font(cfg.KINAKO_FONT_PATH, 35)
    filename_font  = pygame.font.Font(cfg.KINAKO_FONT_PATH, 15)
    # fmt: on

    message_text_surface = message_font.render(MESSAGE_TEXT, True, cfg.COLER_WHITE)

    # 決定するまで
    while not hasDetermined:
        screen.fill(cfg.COLER_BLACK)
        screen.blit(message_text_surface, (40, 40))
        show_image()
        input_event_handling()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
