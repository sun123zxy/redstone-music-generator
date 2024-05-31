from copy import deepcopy
from math import floor
import os

from mcpi import block
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

import rmg
from utils.midi_handler import MIDIHandler
from utils.axis import Axis, player_axis_lhs, player_axis_rhs

import rmg, lkrb, note

if __name__ == "__main__":
    mc = Minecraft()
    midihan = MIDIHandler("my_script/music.mid")
    
    lkrb_kb_config = {
        "mc": mc,
        "axis": player_axis_rhs(mc),
        "notes": list(range(21,109)),
        "vel2force": {v : lkrb.vel2force(127 - v) for v in range(0, 128)},
        "force_dlt": Vec3(0, 2, 4),
        "pbgen": (rmg.KeyboardKey, {
            "facing": player_axis_rhs(mc).fwd_facing,
            "bgen": (lkrb.LkrbCmd, {})
        })
    }
    lkrb_kb = rmg.StaticKeyboard(lkrb_kb_config)
    
    lkrb_kb.generate()
    os.system("pause")
    # ---

    drum_kb_config = {
        "mc": mc,
        "axis": player_axis_rhs(mc),
        "notes": note.drum_mapping.keys(),
        "vel2force": {**{v : 0 for v in range(0, 32)}, **{v : 1 for v in range(32, 64)}, **{v : 2 for v in range(64, 96)}, **{v : 3 for v in range(96, 128)}},
        "force2vel": {0: 16, 1: 48, 2: 80, 3: 112},
        "force_dlt": Vec3(0, 0, 3),
        "pbgen": (rmg.KeyboardKey, {
            "facing": player_axis_rhs(mc).fwd_facing,
            "bgen": (note.NoteDrumCmd, {"vel_factor": 0.8})
        })
    }
    drum_kb = rmg.StaticKeyboard(drum_kb_config)

    drum_kb.generate()
    os.system("pause")
    # ---

    snake_config = {
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
            "pad_block": deepcopy(block.DIRT),
        },
        "mc": mc,
        "axis": player_axis_lhs(mc, Vec3(0, 0, 1)),
        "unit_per_beat": 4,
        "width": 32,
        "fwd": 3,
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
                "height": 30,
                "axgen": lkrb_kb,
                "block_namespace": "minecraft:redstone_block",
                "block_datavalue": 0
            })
        })
    }
    for i in range(1, 6 + 1):
        t= floor((i-1) / 2)
        if i % 2 == 0:
            snake_config["axis"] = player_axis_lhs(mc, Vec3(2, t * 4, 1))
        else:
            snake_config["axis"] = player_axis_rhs(mc, Vec3(2, t * 4, 1))
        # snake_config["pbgen"]["config"]["bgen"]["config"]["block_namespace"] = "coloredredstone:colored_redstone_block"
        # snake_config["pbgen"]["config"]["bgen"]["config"]["block_datavalue"] = i - 1
        snake_config["midi"]["msg_gen"]["track"] = i + 1

        if i == 6:
            snake_config["pbgen"][1]["bgen"][1]["axgen"] = drum_kb

        rmg.Snake(snake_config).generate()