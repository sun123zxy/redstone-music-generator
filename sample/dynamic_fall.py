from copy import deepcopy
from math import floor
import os

from mcpi import block
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

import rmg
from utils.midi_handler import MIDIHandler
from utils.axis import Axis, player_axis_lhs, player_axis_rhs

import rmg, lkrb

if __name__ == "__main__":
    mc = Minecraft()
    midihan = MIDIHandler("my_script/music.mid")
    
    # for i in range(1,2+1):
    for i in range(1, 5 + 1):

        lkrb_kb_config = {
            "midi":{
                "handler": midihan,
                "msg_gen":{
                    "track": i + 1,
                    "st_beat": 53 * 4,
                    "ed_beat": None,
                    "type_switch":{
                        "note_on": True,
                        "note_off": False
                    }
                }
            },
            "mc": mc,
            "axis": player_axis_rhs(mc),
            "notes": list(range(21,109)),
            "unit_per_beat": 4,
            "dlt_per_unit": Vec3(0, 0, 1),
            "magnet": True,
            "pbgen": (rmg.CompactKey, {
                "facing": player_axis_rhs(mc).fwd_facing,
                "bgen": (lkrb.LkrbCmd, {})
            })
        }
        lkrb_kb = rmg.DynamicKeyboard(lkrb_kb_config)
        
        lkrb_kb.generate()

        os.system("pause")
        # ---

        adv_config = {
            "midi": lkrb_kb_config["midi"],
            "base": {
                "on": True,
                "tick_per_repeater": 1,
                "base_block": deepcopy(block.STONE),
                "pad_block": deepcopy(block.DIRT),
            },
            "mc": mc,
            "axis": player_axis_lhs(mc, Vec3(0, 0, 1)),
            "unit_per_beat": 4,
            "width": 4,
            "fwd": 4,
            "magnet": True,
            "mini": False,
            "pbgen": (rmg.SmartAround, {
                "dlt":  [(Vec3(0, 1, 0), True), 
                        (Vec3(0, 0, 1), False),
                        (Vec3(0, 0, -1), False), 
                        (Vec3(1, 0, 0), False), 
                        (Vec3(-1, 0, 0), False),
                        (Vec3(0, 0, 0), True),
                        (Vec3(0, -1, 0), True)],
                "ignore_out_of_range": False,
                "bgen": (rmg.FallCmd, {
                    "height": 5,
                    "axgen": lkrb_kb,
                    "block_namespace": "minecraft:redstone_block",
                    "block_datavalue": 0
                })
            })
        }

        t= floor((i-1) / 2)
        if i % 2 == 0:
            adv_config["axis"] = player_axis_lhs(mc, Vec3(2, t * 4, 1))
        else:
            adv_config["axis"] = player_axis_rhs(mc, Vec3(2, t * 4, 1))
        # adv_config["pbgen"][1]["bgen"][1]["block_namespace"] = "coloredredstone:colored_redstone_block"
        # adv_config["pbgen"][1]["bgen"][1]["block_datavalue"] = i - 1
        adv_config["midi"]["msg_gen"]["track"] = i + 1

        rmg.Advancing(adv_config).generate()

        os.system("pause")
        # ---