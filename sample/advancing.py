from copy import deepcopy
from math import floor

from mcpi import block
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

from utils.midi_handler import MIDIHandler
from utils.axis import Axis, player_axis_lhs, player_axis_rhs

import rmg, lkrb

if __name__ == "__main__":
    mc = Minecraft()
    midihan = MIDIHandler("my_script/music.mid")
    config = {
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
        "pbgen": rmg.SmartAround({
            "dlt":  [(Vec3(0, 1, 0), True), 
                     (Vec3(0, 0, 1), False),
                     (Vec3(0, 0, -1), False), 
                     (Vec3(1, 0, 0), False), 
                     (Vec3(-1, 0, 0), False),
                     (Vec3(0, 0, 0), True),
                     (Vec3(0, -1, 0), True)],
            "ignore_out_of_range": False,
            "bgen": lkrb.LkrbCmd({})
        })
    }
    for i in range(1, 5 + 1):
        t= floor((i-1) / 2)
        if i % 2 == 0:
            config["axis"] = player_axis_lhs(mc, Vec3(2, t * 4, 1))
        else:
            config["axis"] = player_axis_rhs(mc, Vec3(2, t * 4, 1))
        config["midi"]["msg_gen"]["track"] = i + 1
        rmg.Advancing(config).generate()