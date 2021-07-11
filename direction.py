from mine import *

NORTH = 0
EAST  = 1
SOUTH = 2
WEST  = 3

def direction(vec):
    """axis unit vector -> NESW"""
    if vec.z == -1: # Vec3(0, 0, -1)
        return NORTH
    elif vec.z == 1: # Vec3(0, 0, 1)
        return SOUTH
    elif vec.x == 1: # Vec3(1, 0, 0)
        return EAST
    elif vec.x == -1: # Vec3(-1, 0, 0)
        return WEST
    else:
        return -1

def rotToAxisVec(rot):
    """rotation(degrees) -> axis unit vector"""
    vec = Vec3(0, 0, 0)
    if rot <= -135 or rot >= 135: # Back
        vec = Vec3(0, 0, -1)
    elif rot <= -45: # Left
        vec = Vec3(1, 0, 0)
    elif rot <= 45: # Front
        vec = Vec3(0, 0, 1)
    elif rot <= 135: # Right
        vec = Vec3(-1, 0, 0)
    return vec
