from copy import deepcopy
from fractions import Fraction

import mido

from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi.vec3 import Vec3

from utils.config import ConfigLike
from utils.axis import Axis

import rmg

class PBgen(ConfigLike):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
    def pbgen(self, beat: Fraction, msg) -> list: # of (Vec3, block.Block)
        pass
    def pbgens(self, beat: Fraction, msgs) -> list:
        op = []
        for msg in msgs:
            op += self.pbgen(beat, msg)
        return op
    def generate(self, mc: Minecraft, axis: Axis, *args) -> list:
        for pos, blk in self.pbgen(*args):
            mc.setBlockWithNBT(axis.l2g(pos), blk)
    def generates(self, mc: Minecraft, axis: Axis, *args) -> list:
        for pos, blk in self.pbgens(*args):
            mc.setBlockWithNBT(axis.l2g(pos), blk)

class Pgen(ConfigLike):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
    def pgen(self, beat: Fraction, msg: tuple) -> Vec3:
        pass

class Axgen(Pgen):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
    def axgen(self, beat: Fraction, msg: tuple) -> Axis:
        pass
    def pgen(self, *args) -> Vec3:
        return self.axgen(*args).origin

class Bgen(ConfigLike):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
    def bgen(self, beat: Fraction, msg: tuple) -> block.Block:
        pass

class SmartAround(PBgen):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.dlt:list = config["dlt"]
        self.ignore_out_of_range:bool = config.get("ignore_out_of_range")

        bgen, bgen_config = config["bgen"]
        self.bgen: rmg.Bgen = bgen(bgen_config)

    def pbgens(self, beat, msgs, check = lambda: True) -> list:
        cnt = 0
        output = []
        for type, note, velocity, program_id in msgs:
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