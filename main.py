import sys
import threading

import pygame

from interaction import interaction_everyday

img_dict = {}


def pygame_refresh():
    global img_dict
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("The Artifact")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 卸载所有模块
                pygame.quit()
                # 终止程序，确保退出程序
                sys.exit()
        clock.tick(60)
        screen.fill('white')
        for img_id in img_dict:
            img_obj: pygame.Surface = img_dict[img_id][0]
            img_rect: pygame.Rect = img_dict[img_id][1]
            screen.blit(img_obj, img_rect)
        pygame.display.update()


if __name__ == '__main__':
    day_count = 0
    NewBase = None
    global_events = []
    render_queue = []
    pygame_thread = threading.Thread(target=pygame_refresh)
    pygame_thread.start()
    while True:
        if not pygame_thread.is_alive():
            print()
            sys.exit('Pygame Thread Stopped.')
        render_queue, global_events, day_count, img_dict = interaction_everyday(
            render_queue,
            global_events,
            day_count,
            img_dict
        )
