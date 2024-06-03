from fractions import Fraction
from math import floor, ceil
from copy import deepcopy

from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi import block

from utils.midi_handler import MIDIHandler
from utils.axis import Axis
from utils.direction import turn_back
from utils.config import ConfigLike

import rmg

class Snake(ConfigLike):

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        
        self.midihan: MIDIHandler = config["midi"]["handler"]
        self.msg_gen_config = config["midi"]["msg_gen"]
        self.st_beat = config.get("midi").get("msg_gen").get("st_beat") if config.get("midi").get("msg_gen").get("st_beat") != None else 0
        self.ed_beat = config.get("midi").get("msg_gen").get("ed_beat") if config.get("midi").get("msg_gen").get("ed_beat") != None else self.midihan.mx_beat[self.msg_gen_config["track"]]
        self.length = self.ed_beat - self.st_beat
        self.mc: Minecraft = config["mc"]
        self.axis: Axis = config["axis"]
        self.width: int = config["width"]
        self.fwd: int = config["fwd"]
        self.upb: Fraction = config["unit_per_beat"]
        self.magnet = config.get("magnet")

        self.is_gen_base = config.get("base").get("on")
        if self.is_gen_base == True:
            self.tpr: int = config["base"]["tick_per_repeater"]
            self.pad_block: block.Block = config["base"]["pad_block"]
            self.base_block: block.Block = config["base"]["base_block"]
        
        pbgen, pbgen_config = config["pbgen"]
        self.pbgen: rmg.PBgen = pbgen(pbgen_config)
    
    def generate(self) -> None:
        if self.is_gen_base == True:
            for i in range(0, ceil(self.length * self.upb / self.width)):
                z = i * self.fwd
                typ = i % 2
                for x in range(0, self.width * 2 - 1):
                    self.mc.setBlockWithNBT(self.axis.l2g(Vec3(x, 0, z)), self.base_block)
                    if x % 2 == 0:
                        self.mc.setBlockWithNBT(self.axis.l2g(Vec3(x, 1, z)), self.pad_block)
                    else:
                        self.mc.setBlock(self.axis.l2g(Vec3(x, 1, z)),
                                    block.REDSTONE_REPEATER_INACTIVE.id,
                                    (self.tpr - 1) * 4 + (turn_back(self.axis.left_facing) if typ == 0 else turn_back(self.axis.right_facing)))
                edge_x = 0 if typ == 1 else (self.width - 1) * 2
                for dz in range(1, self.fwd):
                    self.mc.setBlockWithNBT(self.axis.l2g(Vec3(edge_x, 0, z + dz)), self.base_block)
                    self.mc.setBlock       (self.axis.l2g(Vec3(edge_x, 1, z + dz)), 55) # REDSTONE_WIRE
                self.mc.setBlock(self.axis.l2g(Vec3(edge_x, 1, z + 1)),
                            block.REDSTONE_REPEATER_INACTIVE.id,
                            (self.tpr - 1) * 4 + turn_back(self.axis.fwd_facing))

        for beat, msgs in self.midihan.msg_gen(self.msg_gen_config):
            if self.magnet == True:
                beat = beat.limit_denominator(self.upb)

            z = floor(beat * self.upb / self.width) * self.fwd
            if floor(beat * self.upb / self.width) % 2 == 0:
                x = round(beat * self.upb) % self.width * 2
            else:
                x = (self.width - 1- round(beat * self.upb) % self.width) * 2
            # print(beat, x, z)
            
            my_axis = Axis(self.axis.l2g(Vec3(x, 1, z)), self.axis.fwd_facing, self.axis.left_facing)

            def is_free(pos: Vec3) -> bool:
                return self.mc.getBlock(my_axis.l2g(pos)) == block.AIR.id
            
            self.pbgen.generates(self.mc, my_axis, beat, msgs, is_free)
        print("<<< snake generated <<<")