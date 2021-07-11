from mcpi.vec3 import *
def vecStepList(st, dlt, step):
    """generate a list of Vec3 by step"""
    ret = []
    for i in range(0, step):
        ret.append(st + dlt * i)
    return ret