import esper

from src.create.prefab_creator import create_enemy_square
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world: esper.World, enemies_data: dict, delta_time: float):
    query = world.get_component(CEnemySpawner)

    for _, c_spw in query:
        c_spw.current_time += delta_time
        for spw_evt in c_spw.spawn_event_data:
            if c_spw.current_time >= spw_evt.time and not spw_evt.triggered:
                spw_evt.triggered = True
                create_enemy_square(
                    world,
                    spw_evt.position,
                    enemies_data[spw_evt.enemy_type],
                )
