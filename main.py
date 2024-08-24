import cProfile
import os
import pstats
import threading

from Engine.Core import Core
from Mechanism.Entity import World
from Mechanism.Game import world_changing

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    core = Core(screen_size=(1280, 720), fps=60, max_queue_size=32)
    world_ = World(core=core, map_image='Assets/city.png')

    wc_thread = threading.Thread(target=world_changing, args=(world_,))

    wc_thread.start()
    world_.start()
    profiler.disable()
    pstats.Stats(
        profiler, stream=open('性能分析.txt', 'w')
    ).sort_stats(pstats.SortKey.CUMULATIVE).print_stats(.3)
    os.abort()
