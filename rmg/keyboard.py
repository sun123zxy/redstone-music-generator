from fractions import Fraction
from math import floor, ceil
from copy import deepcopy

from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi import block

from utils.axis import Axis
from utils.config import ConfigLike
from utils import direction

import rmg

class Keyboard(ConfigLike):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
    def place_axis(self, beat: Fraction, msg: tuple) -> Vec3:
        pass
    def place(self, *args) -> Vec3:
        return self.place_axis(*args).origin

class StaticKeyboard(Keyboard):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.mc:Minecraft = config["mc"]
        self.axis:Axis = config["axis"]
        print("Keyboard will generate by axis:", self.axis)

        self.notes:list = config["notes"]
        self.note2id = {note: i for i, note in enumerate(self.notes)}

        self.vel2force:dict = config["vel2force"]
        self.force2vel:dict = config["force2vel"] if "force2vel" in config else {f: v for v, f in self.vel2force.items()}
        self.forces = self.force2vel.keys()
        self.force_dlt:Vec3 = config["force_dlt"]

        bgen, bgen_config = config["bgen"]
        self.bgen: rmg.Bgen = bgen(bgen_config)
    
    def _place_axis_by_nid_and_force(self, nid, force) -> Axis:
        my_axis = Axis(self.axis.l2g(self.force_dlt * force), self.axis.fwd_facing)
        return Axis(my_axis.l2g(Vec3(nid, 1, 0)), my_axis.fwd_facing)

    def place_axis(self, beat: Fraction, msg: tuple) -> Axis:
        super().place_axis(beat, msg)

        type, note, velocity, program_id = msg
        return self._place_axis_by_nid_and_force(self.note2id[note], self.vel2force[velocity])

    def generate(self) -> None:
        for force in self.forces:
            velocity = self.force2vel[force]
            for i, note in enumerate(self.notes):
                ax = self.place_axis(0, (None, note, velocity, None))

                blk = self.bgen.bgen(None, ("note_on", note, velocity, None))
                self.mc.setBlockWithNBT(ax.l2g(Vec3(0,-1,0)), blk)
                
                blk = deepcopy(block.COMMAND_BLOCK)
                dlt = direction.facing2vec(ax.back_facing)
                blk.nbt = '{Command: "/setblock ~' + str(dlt.x) +  ' ~' + str(dlt.y) + ' ~' + str(dlt.z) + ' minecraft:air"}'
                self.mc.setBlockWithNBT(self.place_axis(0, (None, note, velocity, None)).l2g(Vec3(0,0,1)), blk)
        print("<<< keyboard generated <<<")