from math import floor, ceil, pow
from copy import deepcopy

from mcpi import block

import rmg

drum_mapping = {
    36: ("block.note.basedrum", 1),
    38: ("block.note.snare", 1),
    40: ("block.note.snare", 1.25),
    42: ("block.note.hat", 1),
    46: ("block.note.hat", 1.5),
    49: ("block.note.hat", 1) # Crash
}

class NoteDrumCmd(rmg.Bgen):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.mapping:dict = config["mapping"] if "mapping" in config else drum_mapping
        self.max_vol = config["max_vol"] if "max_vol" in config else 1

    def bgen(self, beat, msg) -> block.Block:
        type, note, velocity, porgram_id = msg
        blk = deepcopy(block.COMMAND_BLOCK)
        name, pitch = self.mapping[note]
        vol = velocity / 128.0 * self.max_vol
        if type == "note_on":
            blk.nbt = '{Command: "/execute @p ~ ~ ~ playsound ' + name + ' voice @p ~ ~ ~ ' + str(vol) + ' ' + str(pitch) + '"}'
        return blk

class NoteCmd(rmg.Bgen):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.name:str = config["name"]
        self.std_note = config["std_note"]
        self.max_vol = config["max_vol"] if "max_vol" in config else 1

    def bgen(self, beat, msg) -> block.Block:
        type, note, velocity, porgram_id = msg
        pitch = pow(2, (note - self.std_note) / 12)
        vol = velocity / 128.0 * self.max_vol
        blk = deepcopy(block.COMMAND_BLOCK)
        if type == "note_on":
            blk.nbt = '{Command: "/execute @p ~ ~ ~ playsound ' + self.name + ' voice @p ~ ~ ~ ' + str(vol) + ' ' + str(pitch) + '"}'
        return blk