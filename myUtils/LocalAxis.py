import copy
from mine import *
from myUtils.direction import *
from myUtils.echo import echo

class LocalAxis:
    """Local Axis"""
    
    def __init__(self, mc, origin, fwd):
        echo("-----LocalAxis-----")
        self.origin = origin
        self.fwd = fwd
        self.back = -self.fwd
        self.left = copy.deepcopy(self.fwd); self.left.rotateLeft()
        self.right = -self.left
        self.up = Vec3(0, 1, 0)
        self.down = -self.up
        echo("Origin: " + str(self.origin))
        echo("Forward: " + str(self.fwd))
        echo("Left: " + str(self.left))
        echo("LocalAxis builded!")
        echo("----------")
    
    def Vec3L(self, t0, t1 = None, t2 = None):
        """localVec3, usage: Vec3L(x,y,z) or Vec3L(vec3)"""
        if t1 == None and t2 == None:
            vec = t0
        else:
            vec = Vec3(t0, t1, t2)
        return self.origin + self.left * vec.x + self.up * vec.y + self.fwd * vec.z

def getPlayerFwdAxis(mc):
    pos = mc.player.getTilePos()
    rot = mc.player.getRotation()
    fwd = rotToAxisVec(rot)
    return LocalAxis(mc, pos + fwd, fwd)