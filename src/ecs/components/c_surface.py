import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)

    @staticmethod
    def as_rectangle(size: pygame.Vector2, color: pygame.Color) -> "CSurface":
        return CSurface(size, color)
