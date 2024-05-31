from math import floor, ceil
from copy import deepcopy

from mcpi import block

import rmg

drum_mapping = {
    35: ("basedrum", 1),
    36: ("basedrum", 1),
    38: ("snare", 1),
    40: ("snare", 1.25),
    42: ("hat", 1),
    46: ("hat", 1.5),
    49: ("hat", 1) # Crash
}

class NoteDrumCmd(rmg.Bgen):
    def __init__(self, config: dict) -> None:
        self.mapping:dict = config["mapping"] if "mapping" in config else drum_mapping
        self.vel_factor = config["vel_factor"] if "vel_factor" in config else 1

    def bgen(self, beat, msg) -> list:
        type, note, velocity, porgram_id = msg
        blk = deepcopy(block.COMMAND_BLOCK)
        name, pitch = self.mapping[note]
        if type == "note_on":
            blk.nbt = '{Command: "/execute @p ~ ~ ~ playsound block.note.' + name + ' voice @p ~ ~ ~ ' + str(velocity/128.0*self.vel_factor) + ' ' + str(pitch) + '"}'
        return blk