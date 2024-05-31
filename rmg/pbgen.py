from copy import deepcopy
from fractions import Fraction

import mido

from mcpi import block
from mcpi.vec3 import Vec3

from utils.config import ConfigLike

class Pbgen(ConfigLike):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
    def pbgen(self, beat: Fraction, msglst: list) -> list:
        pass

class Bgen(ConfigLike):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
    def bgen(self, beat: Fraction, msg: tuple) -> block.Block:
        pass

class SmartAround(Pbgen):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.dlt:list = config["dlt"]
        self.ignore_out_of_range:bool = config.get("ignore_out_of_range")
        self.bgen:Bgen = config["bgen"]

    def pbgen(self, beat, lst: list, check = lambda: True) -> list:
        super().pbgen(beat, lst)

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