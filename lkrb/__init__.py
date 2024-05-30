from math import floor, ceil
from copy import deepcopy

from mcpi import block

import rmg

def force2str(force: int) -> str:
        if force == 0 : return "ppp"
        elif force == 1: return "pp"
        elif force == 2: return "p"
        elif force == 3: return "mp"
        elif force == 4: return "mf"
        elif force == 5: return "f"
        elif force == 6: return "ff"
        elif force == 7: return "fff"
        else: return None

vel_num = 8

def velocity2force(velocity: int) -> int:
        return floor(velocity / 16)
def force2velocity(force: int) -> int:
        return force * 16 + 8

class LkrbCmd(rmg.Bgen):
    def __init__(self, config: dict) -> None:
        pass

    def bgen(self, beat, msg) -> list:
        type, note, velocity, porgram_id = msg
        blk = deepcopy(block.COMMAND_BLOCK)
        if type == "note_on":
            blk.nbt = '{Command: "/execute @p ~ ~ ~ playsound lkrb.piano.p' + str(note) + force2str(velocity2force(velocity)) + ' voice @p ~ ~ ~"}'
        return blk

