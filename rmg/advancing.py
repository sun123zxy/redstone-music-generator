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

class Advancing(ConfigLike):

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
        self.up: int = 0 if config.get("up") == None else config["up"] # use only when turning off base generation
        self.upb: Fraction = config["unit_per_beat"]
        self.magnet = config.get("magnet")
        self.is_mini = config.get("mini")

        self.is_gen_base = config.get("base").get("on")
        if self.is_gen_base == True:
            self.tpr: int = config["base"]["tick_per_repeater"]
            self.pad_block: block.Block = config["base"]["pad_block"]
            self.base_block: block.Block = config["base"]["base_block"]
        
        pbgen, pbgen_config = config["pbgen"]
        self.pbgen: rmg.PBgen = pbgen(pbgen_config)
    
    def generate(self) -> None:
        note_axis = Axis(self.axis.l2g(Vec3(-2, 0, 0)), self.axis.fwd_facing, self.axis.left_facing) if self.is_mini else deepcopy(self.axis)
        
        if self.is_gen_base == True:
            for i in range(0, ceil(self.length * self.upb / self.width)):
                z = i * self.fwd
                for x in range(1, self.width * 2 + 1):
                    if(self.is_mini and x == 1):
                        continue
                    self.mc.setBlockWithNBT(note_axis.l2g(Vec3(x, 0, z)), self.base_block)
                    if x % 2 == 0:
                        self.mc.setBlockWithNBT(note_axis.l2g(Vec3(x, 1, z)), self.pad_block)
                    elif x == 1:
                        self.mc.setBlock(note_axis.l2g(Vec3(x, 1, z)), 55) # REDSTONE_WIRE
                    else:
                        self.mc.setBlock(note_axis.l2g(Vec3(x, 1, z)),
                                    block.REDSTONE_REPEATER_INACTIVE.id,
                                    (self.tpr - 1) * 4 + turn_back(note_axis.left_facing))
                                    
                ret = self.width * self.tpr
                
                if not self.is_mini:
                    self.mc.setBlockWithNBT(self.axis.l2g(Vec3(0, 0, z)), self.base_block)
                    self.mc.setBlockWithNBT(self.axis.l2g(Vec3(0, 1, z)), 55) # REDSTONE_WIRE
                for dz in range(1, self.fwd):
                    self.mc.setBlockWithNBT(self.axis.l2g(Vec3(0, 0, z + dz)), self.base_block)
                    if(ret > 0):
                        self.mc.setBlock(self.axis.l2g(Vec3(0, 1, z + dz)), 
                                                       block.REDSTONE_REPEATER_INACTIVE.id,
                                                       ((4 if ret >= 4 else ret) - 1) * 4 + turn_back(self.axis.fwd_facing))
                    else:
                        self.mc.setBlockWithNBT(self.axis.l2g(Vec3(0, 1, z + dz)), 55)
                    ret -= 4

        for beat, msgs in self.midihan.msg_gen(self.msg_gen_config):
            if self.magnet == True:
                beat = beat.limit_denominator(self.upb)

            z = floor(beat * self.upb / self.width) * self.fwd
            x = (round(beat * self.upb) % self.width + 1) * 2
            # print(beat, x, z)
            
            y = 1 + floor(beat * self.upb / self.width) * self.up

            your_axis = Axis(note_axis.l2g(Vec3(x, y, z)), note_axis.fwd_facing, note_axis.left_facing)

            def is_free(pos: Vec3) -> bool:
                return self.mc.getBlock(your_axis.l2g(pos)) == block.AIR.id
            self.pbgen.generates(self.mc, your_axis, beat, msgs, is_free)
        print("<<< advancing generated <<<")