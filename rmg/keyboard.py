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

class KeyboardKey(rmg.PBgen):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self.facing = config["facing"]    

        bgen, bgen_config = config["bgen"]
        self.bgen = bgen(bgen_config)

    def pbgen(self, beat: Fraction, msglst: list) -> list:
        output = []
        msg = msglst[0]
        blk = self.bgen.bgen(beat, msg)
        output.append((Vec3(0,-1,0), blk))

        blk = deepcopy(block.COMMAND_BLOCK)
        dv = direction.facing2vec(direction.turn_back(self.facing))
        blk.nbt = '{Command: "/setblock ~' + str(dv.x) +  ' ~' + str(dv.y) + ' ~' + str(dv.z) + ' minecraft:air"}'
        output.append((Vec3(0,0,1), blk))
        return output

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

        pbgen, pbgen_config = config["pbgen"]
        self.pbgen: rmg.PBgen = pbgen(pbgen_config)
    
    def _axgen_by_nid_and_force(self, nid, force) -> Axis:
        return Axis(self.axis.l2g(Vec3(nid, 0, 0) + self.force_dlt * force), self.axis.fwd_facing, self.axis.left_facing)

    def axgen(self, beat: Fraction, msg: tuple) -> Axis:
        type, note, velocity, program_id = msg
        return self._axgen_by_nid_and_force(self.note2id[note], self.vel2force[velocity])

    def generate(self) -> None:
        for force in self.forces:
            velocity = self.force2vel[force]
            for note in self.notes:
                msg = ("note_on", note, velocity, 0)
                ax = self.axgen(0, msg)
                for pos, blk in self.pbgen.pbgen(0, [msg]):
                    self.mc.setBlockWithNBT(ax.l2g(pos), blk)
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

        pbgen, pbgen_config = config["pbgen"]
        self.pbgen: rmg.PBgen = pbgen(pbgen_config)
    
    def axgen(self, beat: Fraction, msg: tuple) -> Axis:
        type, note, velocity, program_id = msg
        return Axis(self.axis.l2g(Vec3(self.note2id[note], 0, 0) + self.dlt * floor(beat * self.upb)), self.axis.fwd_facing, self.axis.left_facing)

    def generate(self) -> None:
        for beat, msglst in self.midihan.msg_gen(self.msg_gen_config):
            if self.magnet == True:
                beat = beat.limit_denominator(self.upb)

            for msg in msglst:
                ax = self.axgen(beat, msg)
                for pos, blk in self.pbgen.pbgen(0, [msg]):
                    self.mc.setBlockWithNBT(ax.l2g(pos), blk)
        print("<<< Dynamic Keyboard generated <<<")