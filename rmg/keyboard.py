from fractions import Fraction
from math import floor, ceil
from copy import deepcopy

from mcpi.vec3 import Vec3
from mcpi.minecraft import Minecraft
from mcpi import block

from utils.axis import Axis
from utils.config import ConfigLike
from utils import direction
from utils.midi_handler import MIDIHandler

import rmg

class StaticKeyboard(rmg.Axgen):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.mc:Minecraft = config["mc"]
        self.axis:Axis = config["axis"]
        print("Static Keyboard will generate by axis:", self.axis)

        self.notes:list = config["notes"]
        self.note2id = {note: i for i, note in enumerate(self.notes)}

        self.vel2force:dict = config["vel2force"]
        self.force2vel:dict = config["force2vel"] if "force2vel" in config else {f: v for v, f in self.vel2force.items()}
        self.forces = self.force2vel.keys()
        self.force_dlt:Vec3 = config["force_dlt"]

        bgen, bgen_config = config["bgen"]
        self.bgen: rmg.Bgen = bgen(bgen_config)
    
    def _axgen_by_nid_and_force(self, nid, force) -> Axis:
        my_axis = Axis(self.axis.l2g(self.force_dlt * force), self.axis.fwd_facing)
        return Axis(my_axis.l2g(Vec3(nid, 1, 0)), my_axis.fwd_facing)

    def axgen(self, beat: Fraction, msg: tuple) -> Axis:
        type, note, velocity, program_id = msg
        return self._axgen_by_nid_and_force(self.note2id[note], self.vel2force[velocity])

    def generate(self) -> None:
        for force in self.forces:
            velocity = self.force2vel[force]
            for i, note in enumerate(self.notes):
                ax = self.axgen(0, (None, note, velocity, None))

                blk = self.bgen.bgen(None, ("note_on", note, velocity, None))
                self.mc.setBlockWithNBT(ax.l2g(Vec3(0,-1,0)), blk)
                
                blk = deepcopy(block.COMMAND_BLOCK)
                dv = direction.facing2vec(ax.back_facing)
                blk.nbt = '{Command: "/setblock ~' + str(dv.x) +  ' ~' + str(dv.y) + ' ~' + str(dv.z) + ' minecraft:air"}'
                self.mc.setBlockWithNBT(ax.l2g(Vec3(0,0,1)), blk)
        print("<<< Static Keyboard generated <<<")

class DynamicKeyboard(rmg.Axgen):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.midihan: MIDIHandler = config["midi"]["handler"]
        self.msg_gen_config = config["midi"]["msg_gen"]

        self.mc:Minecraft = config["mc"]
        self.axis:Axis = config["axis"]
        print("Dynamic Keyboard will generate by axis:", self.axis)

        self.notes:list = config["notes"]
        self.note2id = {note: i for i, note in enumerate(self.notes)}
        
        self.upb: Fraction = config["unit_per_beat"]
        self.dlt: Vec3 = config["dlt_per_unit"]
        self.magnet: bool = config["magnet"]

        bgen, bgen_config = config["bgen"]
        self.bgen: rmg.Bgen = bgen(bgen_config)
    
    def axgen(self, beat: Fraction, msg: tuple) -> Axis:
        type, note, velocity, program_id = msg
        return Axis(self.axis.l2g(Vec3(self.note2id[note], 1, 0) + self.dlt * floor(beat * self.upb)), self.axis.fwd_facing)

    def generate(self) -> None:
        for beat, lst in self.midihan.msg_gen(self.msg_gen_config):
            if self.magnet == True:
                beat = beat.limit_denominator(self.upb)

            for msg in lst:
                ax = self.axgen(beat, msg)

                blk = self.bgen.bgen(None, msg)
                self.mc.setBlockWithNBT(ax.l2g(Vec3(0,-1,0)), blk)

                blk = deepcopy(block.COMMAND_BLOCK)
                dv = direction.facing2vec(ax.back_facing)
                blk.nbt = '{Command: "/setblock ~' + str(dv.x) +  ' ~' + str(dv.y) + ' ~' + str(dv.z) + ' minecraft:air"}'
                self.mc.setBlockWithNBT(ax.l2g(Vec3(0,0,1)), blk)
        print("<<< Dynamic Keyboard generated <<<")