import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface


def system_rendering(world: esper.World, screen: pygame.Surface):
    query = world.get_components(CTransform, CSurface)

    for _, components in query:
        c_t: CTransform = components[0]
        c_s: CSurface = components[1]

        screen.blit(c_s.surf, c_t.pos)
