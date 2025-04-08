import esper, pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_bullet_enemy(world: esper.World):
    bullets = world.get_components(CTransform, CSurface, CTagBullet)
    enemies = world.get_components(CTransform, CSurface, CTagEnemy)

    for bullet_entity, (b_trans, b_surf, _) in bullets:
        b_rect = b_surf.surf.get_rect(topleft=b_trans.pos)

        for enemy_entity, (e_trans, e_surf, _) in enemies:
            e_rect = e_surf.surf.get_rect(topleft=e_trans.pos)

            if b_rect.colliderect(e_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)
