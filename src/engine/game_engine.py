import json
import pygame

import esper

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_bullet_screen_limit import system_bullet_screen_limit
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner

from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_screen_limit import system_player_screen_limit
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

from src.create.prefab_creator import create_bullet_square, create_enemy_spawner, create_input_player, create_player_square


class GameEngine:
    def __init__(self) -> None:
        config_num = 'cfg_00' # Cambiar po cfg_01 o cfg_02 para probar los demas json 
        self._load_config_files(config_num)

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])

        self._screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), pygame.SCALED
        )
        self._screen_rect = self._screen.get_rect()

        self.is_running = False

        self._clock = pygame.time.Clock()
        self._framerate = self.window_cfg["framerate"]
        self._delta_time = 0

        self._bg_color = pygame.Color(
            self.window_cfg["bg_color"]["r"],
            self.window_cfg["bg_color"]["g"],
            self.window_cfg["bg_color"]["b"],
            255,
        )

        self._ecs_world = esper.World()

    def _load_config_files(self, config_num):
        with open(f"assets/cfg/{config_num}/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open(f"assets/cfg/{config_num}/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open(f"assets/cfg/{config_num}/level_01.json", encoding="utf-8") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open(f"assets/cfg/{config_num}/player.json", encoding="utf-8") as player_cfg:
            self.player_cfg = json.load(player_cfg)
        with open(f"assets/cfg/{config_num}/bullet.json", encoding="utf-8") as bullet_cfg:
            self.bullet_cfg = json.load(bullet_cfg)

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(self._ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"])
        self._player_c_vel = self._ecs_world.component_for_entity(self._player_entity, CVelocity)
        
        create_enemy_spawner(self._ecs_world, self.level_01_cfg)
        
        create_input_player(self._ecs_world)

    def _calculate_time(self):
        self._clock.tick(self._framerate)
        self._delta_time = self._clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self._ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self._ecs_world, self.enemies_cfg, self._delta_time)
        system_movement(self._ecs_world, self._delta_time)
        system_screen_bounce(self._ecs_world, self._screen_rect)
        system_collision_player_enemy(self._ecs_world, self._player_entity, 
                                      self.level_01_cfg["player_spawn"])
        system_bullet_screen_limit(self._ecs_world, self._screen_rect)
        system_collision_bullet_enemy(self._ecs_world)
        system_player_screen_limit(self._ecs_world, self._screen_rect)
        self._ecs_world._clear_dead_entities()

    def _draw(self):
        self._screen.fill(self._bg_color)

        system_rendering(self._ecs_world, self._screen)

        pygame.display.flip()

    def _clean(self):
        self._ecs_world.clear_database()
        pygame.quit()
        
    def _do_action(self, c_input: CInputCommand):
        print(c_input.name, c_input.phase)
        
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_vel.vel.x += self.player_cfg["input_velocity"]
                
        elif c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_vel.vel.x -= self.player_cfg["input_velocity"]
                
        elif c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.y -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_vel.vel.y += self.player_cfg["input_velocity"]
                
        elif c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_c_vel.vel.y += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_vel.vel.y -= self.player_cfg["input_velocity"]
                
        elif c_input.name == "PLAYER_FIRE":
            if c_input.phase == CommandPhase.END:
                # Acá se tomo en cuenta que solo pueden haber el numero limite de balas
                # presentes en la pantalla. Una vez estas balas sean eliminadas por impactar
                # con un enemigo o po salir de la pantalla, el conteo de balar se renueva a 0
                
                # Basicamente, si el limite son 4 bullets, solo podrán haber 4 bullets EN PANTALLA
                bullet_count = len(self._ecs_world.get_component(CTagBullet))
                max_bullets = self.level_01_cfg["player_spawn"]["max_bullets"]

                if bullet_count < max_bullets:
                    player_transform = self._ecs_world.component_for_entity(self._player_entity, CTransform)
                    player_surface = self._ecs_world.component_for_entity(self._player_entity, CSurface)

                    player_center = player_transform.pos + (pygame.Vector2(player_surface.surf.get_size()) / 2)

                    bullet_direction = pygame.Vector2(c_input.mouse_pos) - player_center
                    if bullet_direction.length() == 0:
                        bullet_direction = pygame.Vector2(0, -1)  # Dirección predeterminada hacia arriba

                    create_bullet_square(self._ecs_world, self.bullet_cfg, player_center, bullet_direction)
