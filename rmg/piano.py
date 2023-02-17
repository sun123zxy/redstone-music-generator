from fractions import Fraction
from math import floor, ceil
from copy import deepcopy

from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi import block

from utils.midi_handler import MIDIHandler
from utils.axis import Axis, player_axis_lhs, player_axis_rhs
from utils import lkrb

import rmg.advancing, rmg.snake

from pbgen import pbgen

class PianoCmd(pbgen.Bgen):
    """!!! IMPORTANT INSTRUCTION!!!
    
    /setworldspawn 0 0 0 before use, or use mcpi_offset to manually eliminate the error"""
    def __init__(self, config) -> None:
        self.axis:Axis = config["axis"]
        self.center:int = config["center"]
        self.height:int = config["height"]

        self.v_type = config["v_type"]
        if self.v_type != "fixed":
            self.v_dlt:Vec3 = config["v_dlt"]
            
        self.mcpi_offset:Vec3 = Vec3(0, 0, 0) if config.get("mcpi_offset") == None else config.get("mcpi_offset")

    def bgen(self, beat, msg: tuple) -> list:
        type, note, velocity, porgram_id = msg
        pos = Vec3(note - self.center, self.height, 0)
        if self.v_type == "fixed":
            pass
        elif self.v_type == "lkrb":
            pos += self.v_dlt * floor(lkrb.velocity2force(velocity))
        pos = self.mcpi_offset + self.axis.l2g(pos)
        blk = deepcopy(block.COMMAND_BLOCK)
        if type == "note_on":
            blk.nbt = '{Command: "/summon falling_block ' + str(pos.x) + ' ' + str(pos.y) + ' ' + str(pos.z) +' {Block:\\"minecraft:redstone_block\\",Time: 1}" }'
            # /summon falling_block ~ ~1 ~ {Block:"minecraft:redstone_block",Time: 1}
        return blk

class PianoKeyboard:
    def __init__(self, config: dict) -> None:
        self.mc:Minecraft = config["mc"]
        self.axis:Axis = config["axis"]
        self.center:int = config["center"]

        self.v_type = config["v_type"]
        if self.v_type != "fixed":
            self.v_dlt:Vec3 = config["v_dlt"]
        else:
            self.velocity:int = config["v_elocity"]

        self.bgen:pbgen.Bgen = config["bgen"]["handler"](config["bgen"].get("config"))

    def generate(self) -> None:
        if self.v_type == "fixed":
            for note in range(0, 128):
                blk = self.bgen.bgen(None, ("note_on", note, self.velocity, None))
                self.mc.setBlockWithNBT(self.axis.l2g(Vec3(note - self.center, 0, 0)), blk)

                blk = deepcopy(block.COMMAND_BLOCK)
                blk.nbt = '{Command: "/setblock ~ ~1 ~ minecraft:air"}'
                self.mc.setBlockWithNBT(self.axis.l2g(Vec3(note - self.center, 1, 1)), blk)
        elif self.v_type == "lkrb":
            for force in range(0, 8):
                my_axis = Axis(self.axis.l2g(self.v_dlt * force), self.axis.fwd_facing, self.axis.left_facing)
                for note in range(0, 128):
                    blk = self.bgen.bgen(None, ("note_on", note, lkrb.force2velocity(force), None))
                    self.mc.setBlockWithNBT(my_axis.l2g(Vec3(note - self.center, 1, 1)), blk)

                    blk = deepcopy(block.COMMAND_BLOCK)
                    blk.nbt = '{Command: "/setblock ~ ~1 ~ minecraft:air"}'
                    self.mc.setBlockWithNBT(my_axis.l2g(Vec3(note - self.center, 0, 0)), blk)
        else:
            print("v_type invalid")
        print("<<< piano keyboard generated <<<")

if __name__ == "__main__":
    mc = Minecraft()
    midihan = MIDIHandler("my_script/anc_rm.mid")
    kb_config = {
        "mc": mc,
        "axis": Axis(player_axis_lhs(mc).l2g(Vec3(0, 0, -40)), player_axis_lhs(mc).back_facing, player_axis_lhs(mc).right_facing),
        "center": 60,
        "v_type": "lkrb",
        "v_dlt": Vec3(0, 2, 3),
        "bgen":{
            "handler": pbgen.LkrbCmd,
            "config": {}
        }
    }
    adv_config = {
        "midi":{
            "handler": midihan,
            "msg_gen":{
                "track": 2 + 1,
                "st_beat": 53 * 4,
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
        "axis": player_axis_lhs(mc, Vec3(0, 0, 1)),
        "unit_per_beat": 4,
        "width": 8,
        "fwd": 3,
        "magnet": True,
        "mini": False,
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
                    "handler": PianoCmd,
                    "config":{
                        "axis": kb_config["axis"],
                        "center": kb_config["center"],
                        "v_type": kb_config["v_type"],
                        "v_dlt": kb_config["v_dlt"],
                        "height": 30
                    }
                }
            }
        }
    }
    PianoKeyboard(kb_config).generate()
    for i in range(1, 5 + 1):
        t= floor((i-1) / 2)
        if i % 2 == 0:
            adv_config["axis"] = player_axis_lhs(mc, Vec3(2, t * 4, 1))
        else:
            adv_config["axis"] = player_axis_rhs(mc, Vec3(2, t * 4, 1))
        adv_config["midi"]["msg_gen"]["track"] = i + 1
        rmg.advancing.Advancing(adv_config).generate()