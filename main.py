import cProfile
import os
import pstats

import pygame

from Mechanism.Config import spr_key_path_pairs, agents_params, game_vars, routines
from Mechanism.Game import Game

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    pygame.init()
    game = Game(spr_key_path_pairs=spr_key_path_pairs)
    game.load_vars(game_vars=game_vars)
    game.load_routines(routines=routines)
    game.new_agent(agent_id='nature')
    game.new_agent(agent_id='player')
    game.init_agents(agents_params=agents_params)
    game.run()
    profiler.disable()
    pstats.Stats(
        profiler, stream=open('Performance.txt', 'w')
    ).sort_stats(pstats.SortKey.CUMULATIVE).print_stats(.3)
    os.abort()
