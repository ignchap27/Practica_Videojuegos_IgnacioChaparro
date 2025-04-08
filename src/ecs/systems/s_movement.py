import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_movement(world: esper.World, delta_time: float):
    query = world.get_components(CTransform, CVelocity)

    for _, components in query:
        c_t: CTransform = components[0]
        c_v: CVelocity = components[1]

        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time
