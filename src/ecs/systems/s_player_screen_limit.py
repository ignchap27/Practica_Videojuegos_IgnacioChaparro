import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_screen_limit(world: esper.World, screen_rect: pygame.Rect):
    components = world.get_components(CTransform, CSurface, CTagPlayer)

    for _, (c_transform, c_surface, _) in components:
        player_rect = c_surface.surf.get_rect(topleft=c_transform.pos)
        player_rect.clamp_ip(screen_rect)
        c_transform.pos.xy = player_rect.topleft
