"""direction

In Minecraft, +z=south, -z=north, +x=east, -x=west"""
from mcpi.vec3 import Vec3

SOUTH = 0
WEST  = 1
NORTH = 2
EAST  = 3

ZERO = Vec3(0, 0, 0)
FWD = Vec3(0, 0, 1)
BACK = Vec3(0, 0, -1)
LEFT = Vec3(1, 0, 0)
RIGHT = Vec3(-1, 0, 0)
UP = Vec3(0, 1, 0)
DOWN = Vec3(0, -1, 0)

def vec2facing(vec: Vec3) -> int:
    if vec == BACK:
        return NORTH
    elif vec == FWD:
        return SOUTH
    elif vec == RIGHT:
        return EAST
    elif vec == LEFT:
        return WEST
    else:
        return -1

def facing2vec(facing: int) -> Vec3:
    if facing == SOUTH:
        return FWD
    elif facing == WEST:
        return RIGHT
    elif facing == NORTH:
        return BACK
    elif facing == EAST:
        return LEFT
    else:
        return ZERO

def turn_left(facing: int) -> int:
    return (facing - 1 + 4) % 4

def turn_right(facing: int) -> int:
    return (facing + 1) % 4

def turn_back(facing: int) -> int:
    return (facing + 2) % 4

def rot2facing(rot: float) -> Vec3:
    """rotation(degree) to facing"""
    vec = Vec3(0, 0, 0)
    if rot <= -135 or rot >= 135:
        vec = NORTH
    elif rot <= -45:
        vec = EAST
    elif rot <= 45:
        vec = SOUTH
    elif rot <= 135:
        vec = WEST
    return vec
