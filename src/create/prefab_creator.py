import random
import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color):
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity, CSurface(size, col))
    world.add_component(cuad_entity, CTransform(pos))
    world.add_component(cuad_entity, CVelocity(vel))
    
    return cuad_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    size = pygame.Vector2(enemy_info["size"]["x"], enemy_info["size"]["y"])
    color = pygame.Color(
        enemy_info["color"]["r"],
        enemy_info["color"]["g"],
        enemy_info["color"]["b"],
        255,
        )
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range_x = vel_min + (random.random() * (vel_max - vel_min))
    vel_range_y = vel_min + (random.random() * (vel_max - vel_min))
    velocity = pygame.Vector2(
        random.choice([-vel_range_x, vel_range_x]),
        random.choice([-vel_range_y, vel_range_y]),
    )
    enemy_entity = create_square(world, size, pos, velocity, color)
    world.add_component(enemy_entity, CTagEnemy())

def create_player_square(world: esper.World, player_info:dict, level_info:dict):
    size = pygame.Vector2(player_info["size"]["x"],
                          player_info["size"]["y"])
    color = pygame.Color(
        player_info["color"]["r"],
        player_info["color"]["g"],
        player_info["color"]["b"],
        255,
        )
    velocity = pygame.Vector2(0, 0) # Empieza quieto
    position = pygame.Vector2(level_info["position"]["x"] - (size.x / 2),
                              level_info["position"]["y"] - (size.x / 2)) 
    
    player_entity = create_square(world, size, position, velocity, color)
    world.add_component(player_entity, CTagPlayer())
    
    return player_entity

def create_bullet_square(world: esper.World, bullet_info:dict, pos:pygame.Vector2, direction: pygame.Vector2):
    size = pygame.Vector2(bullet_info["size"]["x"],
                          bullet_info["size"]["x"])
    
    color = pygame.Color(
        bullet_info["color"]["r"],
        bullet_info["color"]["g"],
        bullet_info["color"]["b"],
        255,
        )
    
    velocity = direction.normalize() *  bullet_info["velocity"]
    
    bullet_entity = create_square(world, size, pos, velocity, color)
    world.add_component(bullet_entity, CTagBullet())
    return bullet_entity
    

def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(level_data["enemy_spawn_events"]))
    
def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_fire = world.create_entity()
    
    world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    world.add_component(input_fire, CInputCommand("PLAYER_FIRE", pygame.MOUSEBUTTONDOWN))