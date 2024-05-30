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

        self.vel2force:function = config["vel2force"]
        self.force2vel:function = config["force2vel"]
        self.force_num = config["force_num"]
        self.force_dlt = config["force_dlt"]

        self.bgen:rmg.Bgen = config["bgen"]
    
    def place_axis(self, beat: Fraction, msg: tuple) -> Axis:
        type, note, velocity, program_id = msg
        my_axis = Axis(self.axis.l2g(self.force_dlt * self.vel2force(velocity)), self.axis.fwd_facing)
        return Axis(my_axis.l2g(Vec3(note, 1, 0)), my_axis.fwd_facing)

    def generate(self) -> None:
        for force in set(map(self.vel2force, range(0, 128))):
            velocity = self.force2vel(force)
            for note in self.notes:
                blk = self.bgen.bgen(None, ("note_on", note, velocity, None))
                self.mc.setBlockWithNBT(self.place_axis(0, (None, note, velocity, None)).l2g(Vec3(0,0,1)), blk)
                
                blk = deepcopy(block.COMMAND_BLOCK)
                blk.nbt = '{Command: "/setblock ~ ~1 ~ minecraft:air"}'
                self.mc.setBlockWithNBT(self.place_axis(0, (None, note, velocity, None)).l2g(Vec3(0,-1,0)), blk)
        print("<<< keyboard generated <<<")