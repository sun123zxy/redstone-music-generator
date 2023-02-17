from copy import deepcopy
from fractions import Fraction

import mido

from mcpi import block
from mcpi.vec3 import Vec3

from utils import lkrb

class Pbgen:
    def __init__(self, config: dict) -> None:
        pass
    def pbgen(self, beat: Fraction, msglst: list) -> list:
        pass

class Bgen:
    def __init__(self, config: dict) -> None:
        pass
    def bgen(self, beat: Fraction, msg: tuple) -> block.Block:
        pass

class SmartAround(Pbgen):
    def __init__(self, config: dict) -> None:
        self.dlt:list = config["dlt"]
        self.ignore_out_of_range:bool = config.get("ignore_out_of_range")
        self.bgen:Bgen = config["bgen"]["handler"](config["bgen"].get("config"))

    def pbgen(self, beat, lst: list, check = lambda: True) -> list:
        cnt = 0
        output = []
        for type, note, velocity, program_id in lst:
            blk = self.bgen.bgen(beat, (type, note, velocity, program_id))
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

class LkrbCmd(Bgen):
    def __init__(self, config: dict) -> None:
        pass

    def bgen(self, beat, msg) -> list:
        type, note, velocity, porgram_id = msg
        blk = deepcopy(block.COMMAND_BLOCK)
        if type == "note_on":
            blk.nbt = '{Command: "/execute @p ~ ~ ~ playsound lkrb.piano.p' + str(note) + lkrb.force2str(lkrb.velocity2force(velocity)) + ' voice @p ~ ~ ~"}'
        return blk