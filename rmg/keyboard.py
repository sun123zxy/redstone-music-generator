from fractions import Fraction
from math import floor, ceil
from copy import deepcopy

from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi import block

from utils.axis import Axis

import rmg

class Keyboard:
    def __init__(self, config: dict) -> None:
        pass
    def place_axis(self, beat: Fraction, msg: tuple) -> Vec3:
        pass
    def place(self, *args) -> Vec3:
        return self.place_axis(*args).origin

class StaticKeyboard(Keyboard):
    def __init__(self, config: dict) -> None:
        self.mc:Minecraft = config["mc"]
        self.axis:Axis = config["axis"]
        print("Notice! Keyboard will generate by axis:", self.axis)

        self.notes:list = config["notes"]
        self.vel_num:list = config["vel_num"]
        self.vel_dlt:Vec3 = config["vel_dlt"]

        self.bgen:rmg.Bgen = config["bgen"]
    
    def place_axis(self, beat: Fraction, msg: tuple) -> Axis:
        type, note, velocity, program_id = msg
        force = floor(velocity / (128.0 / self.vel_num))
        my_axis = Axis(self.axis.l2g(self.vel_dlt * (self.vel_num - 1 - force)), self.axis.fwd_facing)
        return Axis(my_axis.l2g(Vec3(note, 1, 0)), my_axis.fwd_facing)

    def generate(self) -> None:
        for force in range(0, self.vel_num):
            velocity = floor((force + 0.5) * 128 / self.vel_num)
            for note in self.notes:
                blk = self.bgen.bgen(None, ("note_on", note, velocity, None))
                self.mc.setBlockWithNBT(self.place_axis(0, (None, note, velocity, None)).l2g(Vec3(0,0,1)), blk)
                
                blk = deepcopy(block.COMMAND_BLOCK)
                blk.nbt = '{Command: "/setblock ~ ~1 ~ minecraft:air"}'
                self.mc.setBlockWithNBT(self.place_axis(0, (None, note, velocity, None)).l2g(Vec3(0,-1,0)), blk)
        print("<<< keyboard generated <<<")