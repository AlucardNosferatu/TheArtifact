import threading

import pygame

from Engine.Controller import EventController
from Engine.Renderer import Renderer


class Core:
    def __init__(self, game_obj, screen_size=(1280, 720), fps=60, max_queue_size=256, recent_amount=16):
        self.fps = fps
        self.screen_size = screen_size
        self.max_queue_size = max_queue_size
        self.recent_amount = recent_amount
        self.queue_lock = threading.Lock()
        self.clock = pygame.time.Clock()
        self.params = {}  # 游戏机制的全局参数字典
        self.event_controller = None
        self.renderer = Renderer(self.screen_size)  # 渲染器实例
        self.event_controller = EventController(self.max_queue_size)
        self.world_routine = []
        self.ui_routine = []
        self.recent_input = []
        self.game_obj = game_obj
        self.game_obj.load_engine(engine_ptr=self)

    def engine_run(self):
        pygame.init()
        try:
            self.game_obj.ignite()
            while True:
                self.event_controller.handle_events()
                self.get_recent_input()
                self.renderer.render_frame()
                for event in self.recent_input:
                    e = event[0]
                    if e.type == pygame.QUIT:
                        return
                # 维持tick频率为30Hz
                self.clock.tick(self.fps)
        finally:
            pygame.quit()

    def get_recent_input(self):
        self.recent_input.clear()
        for _ in range(self.recent_amount):
            if len(self.event_controller.event_queue) > 0:
                self.recent_input.append(self.event_controller.event_queue.pop(0))
