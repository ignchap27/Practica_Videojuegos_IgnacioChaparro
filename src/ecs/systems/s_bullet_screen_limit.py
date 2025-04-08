import esper, pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_bullet_screen_limit(world: esper.World, screen_rect: pygame.Rect):
    components = world.get_components(CTransform, CSurface, CTagBullet)
    for bullet, (c_t, c_s, _) in components:
        rect = c_s.surf.get_rect(topleft=c_t.pos)
        if not screen_rect.colliderect(rect):
            world.delete_entity(bullet)
