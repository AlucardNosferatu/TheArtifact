import pygame


class Renderer:
    def __init__(self, screen_size, core):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.running = True
        self.world_draw = {}
        self.ui_draw = {}
        self.core = core

    def render_frame(self):
        # Clear the screen with a black background
        self.screen.fill((0, 0, 0))
        # Draw all objects from the global dictionary
        wd = self.world_draw.copy()
        for i in range(0, 9):
            for key, item in wd.items():
                # Blit the surface to the screen at the given position
                if key is not None and key[0] == str(i):
                    if type(item) is list and item[0] == 'DELETE_THIS':
                        del self.world_draw[key]
                        self.core.remove_routine(func=item[1].render_routine, r_type='w')
                        self.core.remove_routine(func=item[1].delete_routine, r_type='w')
                    else:
                        (surface, position, visible, angle, new_size, flip) = item
                        if visible:
                            self.screen.blit(
                                surface,
                                (
                                    position[0] - round(surface.get_width() * 0.5),
                                    position[1] - round(surface.get_height() * 0.5)
                                )
                            )
        ud = self.ui_draw.copy()
        for key, item in ud.items():
            # Blit the surface to the screen at the given position
            if key is not None:
                if type(item) is list and item[0] == 'DELETE_THIS':
                    del self.ui_draw[key]
                    self.core.remove_routine(func=item[1].render_routine, r_type='u')
                    self.core.remove_routine(func=item[1].delete_routine, r_type='u')
                else:
                    (surface, position, visible, angle, new_size, flip) = item
                    if visible:
                        self.screen.blit(
                            surface,
                            (
                                position[0] - round(surface.get_width() * 0.5),
                                position[1] - round(surface.get_height() * 0.5)
                            )
                        )
            # Update the display
        pygame.display.flip()
