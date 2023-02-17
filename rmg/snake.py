from fractions import Fraction
from math import floor
from copy import deepcopy

from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi import block

from utils.midi_handler import MIDIHandler
from utils.axis import Axis, player_axis_lhs, player_axis_rhs
from utils.direction import turn_back

from pbgen import pbgen

class Snake:

    def __init__(self, config: dict) -> None:
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
        
        self.pbgen: pbgen.Pbgen = config["pbgen"]["handler"](config["pbgen"]["config"])
    
    def generate(self) -> None:
        if self.is_gen_base == True:
            for i in range(0, floor(self.length * self.upb / self.width + 1)):
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

        for beat, lst in self.midihan.msg_gen(self.msg_gen_config):
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
            pblst = self.pbgen.pbgen(beat, lst, is_free)

            for pos, blk in pblst:
                self.mc.setBlockWithNBT(my_axis.l2g(pos), blk)
        print("<<< snake generated <<<")


if __name__ == "__main__":
    mc = Minecraft()
    midihan = MIDIHandler("my_script/anc_rm.mid")
    configA = {
        "midi":{
            "handler": midihan,
            "msg_gen":{
                "track": 2 + 1,
                "st_beat": None,
                "ed_beat": None,
                "type_switch":{
                    "note_on": True,
                    "note_off": False
                }
            }
        },
        "base": {
            "on": True,
            "tick_per_repeater": 1,
            "base_block": deepcopy(block.STONE),
            "pad_block": deepcopy(block.REDSTONE_LAMP_INACTIVE),
        },
        "mc": mc,
        "axis": player_axis_lhs(mc, Vec3(1, 0, 1)),
        "unit_per_beat": 4,
        "width": 8,
        "fwd": 3,
        "magnet": True,
        "pbgen":{
            "handler": pbgen.SmartAround,
            "config": {
                "dlt":  [(Vec3(0, 1, 0), True), 
                         (Vec3(0, 0, 1), False),
                         (Vec3(0, 0, -1), False), 
                         (Vec3(1, 0, 0), False), 
                         (Vec3(-1, 0, 0), False),
                         (Vec3(0, 0, 0), True),
                         (Vec3(0, -1, 0), True)],
                "ignore_out_of_range": False,
                "bgen":{
                    "handler": pbgen.LkrbCmd,
                    "config": {}
                }
            }
        }
    }
    for i in range(1, 5 + 1):
        t= floor((i-1) / 2)
        if i % 2 == 0:
            configA["axis"] = player_axis_lhs(mc, Vec3(2, t * 4, 1))
        else:
            configA["axis"] = player_axis_rhs(mc, Vec3(2, t * 4, 1))
        configA["midi"]["msg_gen"]["track"] = i + 1
        Snake(configA).generate()