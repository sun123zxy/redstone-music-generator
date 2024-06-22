from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft

from utils import direction

class Axis:
    def __init__(self, origin: Vec3, fwd_facing: int, left_facing: int = None) -> None:
        if left_facing == None:
            left_facing = direction.turn_left(fwd_facing)
        self.origin = origin

        self.fwd_facing = fwd_facing
        self.fwd = direction.facing2vec(fwd_facing)

        self.back_facing = direction.turn_back(fwd_facing)
        self.back = -self.fwd

        self.left_facing = left_facing
        self.left = direction.facing2vec(left_facing)

        self.right_facing = direction.turn_back(left_facing)
        self.right = -self.left

        self.up = direction.UP
        self.down = direction.DOWN
    def l2g(self, vec: Vec3) -> Vec3:
        """vector local to global"""
        return self.origin + self.left * vec.x + self.up * vec.y + self.fwd * vec.z
    def __repr__(self):
        return "Axis({}, {}, {})".format(str(self.origin), str(self.fwd), str(self.left))

def player_axis_lhs(mc: Minecraft, offset: Vec3 = Vec3(0, 0, 0)) -> Axis:
    pos = mc.player.getTilePos()
    rot = mc.player.getRotation()
    fwd_facing = direction.rot2facing(rot)
    axis = Axis(pos, fwd_facing, direction.turn_left(fwd_facing))
    return Axis(axis.l2g(offset), axis.fwd_facing, axis.left_facing)

def player_axis_rhs(mc: Minecraft, offset: Vec3 = Vec3(0, 0, 0)) -> Axis:
    pos = mc.player.getTilePos()
    rot = mc.player.getRotation()
    fwd_facing = direction.rot2facing(rot)
    axis = Axis(pos, fwd_facing, direction.turn_right(fwd_facing))
    return Axis(axis.l2g(offset), axis.fwd_facing, axis.left_facing)

if __name__ == "__main__":
    mc = Minecraft()
    axis = player_axis_lhs(mc)
    print(axis)