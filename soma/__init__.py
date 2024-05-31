"""
Abandoned
"""
from copy import deepcopy
import mido

from mcpi.vec3 import Vec3
from mcpi import block

import rmg

class SomaSmartAround(rmg.PBgen):
    def __init__(self, config: dict) -> None:
        self.program: str = config["program"]
        if self.program == "auto":
            self.auto_map = config["auto_map"]
        self.dlt = config["dlt"]
        self.ignore_out_of_range = config.get("ignore_out_of_range")
    
    def pbgen(self, lst: list, check = lambda: True) -> list:
        cnt = 0
        output = []
        for type, note, velocity, program_id in lst:
            if self.program == "auto":
                program = self.auto_map[program_id]
            else:
                program = self.program
            blk = deepcopy(block.COMMAND_BLOCK)
            if type == "note_on":
                blk.nbt ='{Command: "/execute @p ~ ~ ~ playsound ' + program + '.' + str(note) + ' voice @p ~ ~ ~ ' + str(velocity/128) + '"}'
            elif type == "note_off":
                blk.nbt ='{Command: "/stopsound @p voice ' + program + '.' + str(note) + '"}'
            while True:
                if cnt >= len(self.dlt):
                    if self.ignore_out_of_range == True: break
                if self.dlt[cnt][1] == True or check(self.dlt[cnt][0]):
                    output.append((self.dlt[cnt][0], blk))
                    break
                else:
                    cnt += 1
            cnt += 1
        return output

from math import floor

from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi import block

from utils.midi_handler import MIDIHandler
from utils.axis import Axis, player_axis_lhs, player_axis_rhs
from rmg.snake import Snake

if __name__ == "__main__":
    mc = Minecraft()
    midihan = MIDIHandler("my_script/th07_10_converted.mid")
    configA = {
        "midi":{
            "handler": midihan,
            "msg_gen":{
                "track": 2 + 1,
                "st_beat": None,
                "ed_beat": None,
                "type_switch":{
                    "note_on": True,
                    "note_off": True
                }
            }
        },
        "base": {
            "on": True,
            "tick_per_repeater": 1,
            "base_block": deepcopy(block.STONE)
        },
        "mc": mc,
        "axis": player_axis_lhs(mc, Vec3(1, 0, 1)),
        "unit_per_beat": 4,
        "width": 8,
        "fwd": 3,
        "magnet": True,
        "pbgen":{
            "handler": SomaSmartAround,
            "config": {
                "program": "auto",
                "auto_map": {
                    0: "1c",
                    1: "2c",
                    4: "5", # Electric
                    8: "9c",
                    14: "15", # Tubular
                    25: "26c",
                    36: "37", # Slap Bass 1
                    48: "49c",
                    52: "53c",
                    73: "74c"
                },
                "dlt":  [(Vec3(0, 1, 0), True), 
                         (Vec3(0, 0, 1), False),
                         (Vec3(0, 0, -1), False), 
                         (Vec3(1, 0, 0), False), 
                         (Vec3(-1, 0, 0), False), 
                         (Vec3(0, 0, 0), True), 
                         (Vec3(0, -1, 0), True)],
                "ignore_out_of_range": True
            }
        }
    }
    for i in range(1, 13):
        t= floor((i-1) / 2)
        if i == 10:
            configA["pbgen"]["config"]["program"] = "0"
        else:
            configA["pbgen"]["config"]["program"] = "auto"
        if i % 2 == 0:
            configA["axis"] = player_axis_lhs(mc, Vec3(2, t * 4, 1))
        else:
            configA["axis"] = player_axis_rhs(mc, Vec3(2, t * 4, 1))
        configA["midi"]["msg_gen"]["track"] = i + 1
        Snake(configA).generate()