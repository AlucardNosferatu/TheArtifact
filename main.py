import pygame as pygame

from Engine.Core import Core
from Mechanism.Game import Game

if __name__ == '__main__':
    game = Game()
    core = Core(pygame=pygame, game_obj=game)
    game.load_routine()
    core.engine_run()
