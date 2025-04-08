import json
import pygame

import esper

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner

from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

from src.create.prefab_creator import create_enemy_spawner


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])

        self._screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), pygame.SCALED
        )
        self._screen_rect = self._screen.get_frect()

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

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)

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
        create_enemy_spawner(self._ecs_world, self.level_01_cfg)

    def _calculate_time(self):
        self._clock.tick(self._framerate)
        self._delta_time = self._clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self._ecs_world, self.enemies_cfg, self._delta_time)
        system_movement(self._ecs_world, self._delta_time)
        system_screen_bounce(self._ecs_world, self._screen_rect)

    def _draw(self):
        self._screen.fill(self._bg_color)

        system_rendering(self._ecs_world, self._screen)

        pygame.display.flip()

    def _clean(self):
        pygame.quit()
