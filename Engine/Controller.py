import time

import pygame
from pygame import NOEVENT, MOUSEMOTION


class EventController:
    def __init__(self, max_queue_size):
        self.max_queue_size = max_queue_size
        self.running = True
        self.event_queue = []

    def handle_events(self):
        # 获取当前时间戳
        timestamp = time.time()
        # 获取事件
        # 添加事件到队列
        # 将新事件和时间戳加入队列
        new_event = [
            (event, timestamp) for event in pygame.event.get() if event.type != NOEVENT and event.type != MOUSEMOTION
        ]
        self.event_queue += new_event
        # 如果队列已满，丢弃队首的事件
        self.event_queue = self.event_queue[max(0, len(self.event_queue) - self.max_queue_size):]
