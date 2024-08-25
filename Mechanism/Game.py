import threading
import time

from Engine.Core import Core
from Engine.UI import Sprite
from Mechanism.Agent import Agent, Nature, Player
from Mechanism.Entity import World


class Game:
    def __init__(self, spr_key_path_pairs=None):
        self.wml_thread = None
        self.vars = {}
        self.routines = {}
        self.agents = {}
        self.agents_params = {}
        self.core = Core(screen_size=(1280, 720), fps=60, max_queue_size=32)
        self.core.params['game_vars'] = self.vars
        if spr_key_path_pairs is not None:
            self.precache_sprites(key_path_pairs=spr_key_path_pairs)
        self.world = World(core=self.core, map_image='#city')

    def run(self):
        self.start_world_module_loop()
        self.world.io_module_loop()

    @staticmethod
    def precache_sprites(key_path_pairs):
        for key_path_pair in key_path_pairs:
            key = key_path_pair[0]
            image_path = key_path_pair[1]
            Sprite.precache_surfaces(key=key, image_path=image_path)

    def load_vars(self, game_vars: dict):
        for key, val in game_vars.items():
            self.vars[key] = val

    def load_routines(self, routines):
        for key, val in routines.items():
            self.routines[key] = val

    def init_agents(self, agents_params):
        self.agents_params = agents_params
        for agent_id in self.agents.keys():
            self.init_agent(agent_id=agent_id, agent_params=self.agents_params[agent_id])

    def new_agent(self, agent_id):
        if agent_id == 'player':
            agent = Player(world=self.world)
        elif agent_id == 'nature':
            agent = Nature(world=self.world)
        else:
            agent = Agent(world=self.world, agent_id=agent_id)
        self.agents[agent_id] = agent

    def init_agent(self, agent_id, agent_params):
        agent = self.agents[agent_id]
        ent_types = agent_params['ent_types']
        for ent_type in ent_types:
            render_order = ent_type['render_order']
            image_path = ent_type['image_path']
            type_name = ent_type['type_name']
            agent.update_ent_type(render_order=render_order, image_path=image_path, type_name=type_name)
        extra_routines = agent_params['extra_routines']
        for extra_routine in extra_routines:
            if extra_routine not in agent.world_modules:
                agent.world_modules.append(extra_routine)
        if type(agent) is Player:
            sti_list = agent_params['sti']
            for sti in sti_list:
                sti: dict
                sti_id = sti['sti_id']
                sti_type = sti['sti_type']
                image_path = sti.get('image_path', None)
                x = sti.get('x', None)
                y = sti.get('y', None)
                trigger_key = sti.get('trigger_key', None)
                mouse_r_type = sti.get('mouse_r_type', None)
                text = sti.get('text', None)
                callback = sti.get('callback', None)
                if callback is not None:
                    callback = self.routines[callback]
                agent.add_sti(
                    sti_id=sti_id, sti_type=sti_type, image_path=image_path, x=x, y=y, callback=callback,
                    trigger_key=trigger_key, mouse_r_type=mouse_r_type, text=text
                )

    def world_module_loop(self):
        while True:
            for agent_id in self.agents.keys():
                world_modules = self.agents[agent_id].world_modules.copy()
                for world_module in world_modules:
                    world_module(game=self)
            time.sleep(0.01)

    def start_world_module_loop(self):
        self.wml_thread = threading.Thread(target=self.world_module_loop)
        self.wml_thread.start()
