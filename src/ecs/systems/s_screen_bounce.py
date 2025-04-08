import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface


def system_screen_bounce(world: esper.World, screen_rect: pygame.FRect):
    query = world.get_components(CTransform, CVelocity, CSurface)

    for _, components in query:
        c_t: CTransform = components[0]
        c_v: CVelocity = components[1]
        c_s: CSurface = components[2]

        cuad_rect = c_s.surf.get_frect(topleft=c_t.pos)
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
            c_v.vel.x *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.x = cuad_rect.x

        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            c_v.vel.y *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.y = cuad_rect.y
