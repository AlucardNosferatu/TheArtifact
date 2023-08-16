import os
import time

import cocos
import cv2
import keyboard
import numpy as np
from cocos.actions import ScaleBy, Repeat, Reverse, RotateBy


def move(direction, player):
    speed = 2
    if 'up' in direction:
        player[1] -= speed
    if 'down' in direction:
        player[1] += speed
    if 'left' in direction:
        player[0] -= speed
    if 'right' in direction:
        player[0] += speed


def play_by_cmd():
    w, h = 32, 32
    # x, y
    player = [round(w / 2), round(h / 2)]
    keyboard.add_hotkey(hotkey='up', callback=move, args=('up', player))
    keyboard.add_hotkey(hotkey='down', callback=move, args=('down', player))
    keyboard.add_hotkey(hotkey='left', callback=move, args=('left', player))
    keyboard.add_hotkey(hotkey='right', callback=move, args=('right', player))
    while True:
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        for i in range(h):
            for j in range(w):
                if j == player[0] and i == player[1]:
                    print('@', end='  ')
                else:
                    print('_', end='  ')
            print()
        time.sleep(0.01)


def play_by_cv2():
    w, h = 128, 128
    # x, y
    player = [round(w / 2), round(h / 2)]
    keys = ['up', 'down', 'left', 'right', 'up+left', 'up+right', 'down+left', 'down+right']
    for key in keys:
        keyboard.add_hotkey(hotkey=key, callback=move, args=(key, player), suppress=True)
    while True:
        row = [[255, 255, 255].copy() for _ in range(w)]
        canvas = np.array([row.copy() for _ in range(h)]).astype(np.uint8)
        player[0] = min(max(0, player[0]), w - 1)
        player[1] = min(max(0, player[1]), h - 1)
        cv2.circle(canvas, tuple(player), 32, (0, 0, 255), 8)
        cv2.imshow('test', canvas)
        cv2.waitKey(1)


class HelloWorld(cocos.layer.ColorLayer):
    def __init__(self):
        super().__init__(r=64, g=64, b=224, a=255, width=128, height=128)
        sprite = cocos.sprite.Sprite('rws.png')
        sprite.position = 64, 64
        sprite.scale = 0.125
        self.add(sprite, z=1)
        scale = ScaleBy(1, duration=2)
        sprite.do(Repeat(scale + Reverse(scale)))


def play_by_cocos():
    cocos.director.director.init(width=128, height=128)
    hello_layer = HelloWorld()
    hello_layer.do(RotateBy(360, duration=10))
    main_scene = cocos.scene.Scene(hello_layer)
    cocos.director.director.run(main_scene)


if __name__ == '__main__':
    play_by_cocos()
