import cProfile
import os
import pstats
import threading

import pygame

from Engine.Core import Core
from Engine.UI import Sprite
from Mechanism.Entity import World
from Mechanism.Game import world_changing

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    pygame.init()
    core = Core(screen_size=(1280, 720), fps=30, max_queue_size=32)

    Sprite.precache_surfaces(key='#city', image_path='Assets/city.png')
    Sprite.precache_surfaces(key='#button', image_path='Assets/btn.png')
    Sprite.precache_surfaces(key='#jet', image_path='Assets/F-5E.png')
    # Sprite.precache_surfaces(key='#city', image_path='Assets/wifi.png')
    # Sprite.precache_surfaces(key='#button', image_path='Assets/test.png')
    # Sprite.precache_surfaces(key='#jet', image_path='Assets/testcases.png')

    Sprite.precache_surfaces(key='#bullet', image_path='Assets/bullet.png')
    Sprite.precache_surfaces(key='#missile', image_path='Assets/missile.png')
    Sprite.precache_surfaces(key='#target', image_path='Assets/target.png')

    world_ = World(core=core, map_image='#city')

    wc_thread = threading.Thread(target=world_changing, args=(world_,))

    wc_thread.start()
    world_.start()
    profiler.disable()
    pstats.Stats(
        profiler, stream=open('Performance.txt', 'w')
    ).sort_stats(pstats.SortKey.CUMULATIVE).print_stats(.3)
    os.abort()
