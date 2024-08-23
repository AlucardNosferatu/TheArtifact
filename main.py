import os
import threading

from Engine.Core import Core
from Mechanism.Entity import World
from Mechanism.Game import world_changing

if __name__ == '__main__':
    core = Core()
    world_ = World(core=core, map_image='Assets/city.png')

    wc_thread = threading.Thread(target=world_changing, args=(world_,))

    wc_thread.start()
    world_.start()
    os.abort()
