from fractions import Fraction
from math import floor, ceil
from copy import deepcopy

from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi import block

import rmg

class FallCmd(rmg.Bgen):
    """!!! IMPORTANT INSTRUCTION!!!
    
    /setworldspawn 0 0 0 before use, or use mcpi_offset to manually eliminate the error"""
    def __init__(self, config:dict) -> None:
        super().__init__(config)

        self.height:int = config["height"]
        
        self.pgen:rmg.Pgen = config["axgen"]
        
        self.blk_namespace = config["block_namespace"]
        self.blk_datavalue = 0 if config.get("block_datavalue") == None else config.get("block_datavalue")
            
        self.mcpi_offset:Vec3 = Vec3(0, 0, 0) if config.get("mcpi_offset") == None else config.get("mcpi_offset")

    def bgen(self, beat, msg: tuple) -> list:
        super().bgen(beat, msg)

        type, note, velocity, porgram_id = msg
        pos = self.mcpi_offset + self.pgen.pgen(beat, msg) + Vec3(0, self.height, 0)
        blk = deepcopy(block.COMMAND_BLOCK)
        if type == "note_on":
            blk.nbt = '{Command: "/summon falling_block ' + str(pos.x) + ' ' + str(pos.y) + ' ' + str(pos.z) + ' {Block:\\"' + self.blk_namespace + '\\",Data:' + str(self.blk_datavalue) + ',Time:1}"}'
            # /summon falling_block ~ ~1 ~ {Block:"minecraft:redstone_block",Time: 1}
        return blk