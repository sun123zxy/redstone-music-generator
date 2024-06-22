from copy import deepcopy
from math import floor
import os
from fractions import Fraction

from mcpi import block
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

import rmg
from utils.midi_handler import MIDIHandler
from utils.axis import Axis, player_axis_lhs, player_axis_rhs

import rmg

if __name__ == "__main__":
    mc = Minecraft()
    
    print("confirm pos1")
    os.system("pause")
    pos1 = player_axis_rhs(mc).origin
    print(pos1)
    print("confirm pos2")
    os.system("pause")
    pos2 = player_axis_rhs(mc).origin
    print(pos2)

    x1, x2 = min(pos1.x, pos2.x), max(pos1.x, pos2.x)
    y1, y2 = min(pos1.y, pos2.y), max(pos1.y, pos2.y)
    z1, z2 = min(pos1.z, pos2.z), max(pos1.z, pos2.z)

    for x in range(x1,x2+1):
        for y in range(y1,y2+1):
            for z in range(z1,z2+1):
                pos = Vec3(x,y,z)
                block.Block
                blk = mc.getBlockWithNBT(x,y,z)
                if blk.id == block.COMMAND_BLOCK.id:
                    ir = blk.nbt.find(" voice @p ~ ~ ~")
                    il = blk.nbt.find("lkrb.piano.p")
                    print(il,ir,blk.nbt[il:ir])
                    if il != -1 and ir != -1:
                        while not (ord(blk.nbt[ir]) >= ord("0") and ord(blk.nbt[ir]) <= ord("9")): ir -= 1
                        ir += 1
                        il += 12
                        pitch = int(blk.nbt[il:ir])
                        blk.nbt =  blk.nbt[0:il] + str(pitch + 1) + blk.nbt[ir:]
                        mc.setBlockWithNBT(pos, blk)
                        print(pitch, "->", pitch + 1, "at", pos)