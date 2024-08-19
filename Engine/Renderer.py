import pygame


class Renderer:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.running = True
        self.draw_dict = {}

    def render_frame(self):
        # Clear the screen with a black background
        self.screen.fill((0, 0, 0))
        # Draw all objects from the global dictionary
        for key, item in self.draw_dict.items():
            # Blit the surface to the screen at the given position
            if key is not None:
                (surface, position, visible, angle, magnify, flip) = item
                if visible:
                    s = pygame.transform.rotate(surface=surface, angle=angle)
                    s = pygame.transform.scale(surface=s, size=magnify)
                    s = pygame.transform.flip(surface=s, flip_x=flip[0], flip_y=flip[1])
                    self.screen.blit(
                        s,
                        (
                            position[0] - round(s.get_width() * 0.5),
                            position[1] - round(s.get_height() * 0.5)
                        )
                    )
        # Update the display
        pygame.display.flip()
