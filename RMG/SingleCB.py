from .RMG import *
from myUtils.vecStepList import *

class SingleCB(RMG.DeleManager.NoteDele):
    """A NoteDele which generate single command block for a note."""

    class GenManager():
        class PosGen(RMG.DeleManager.NoteDele):
            """Generate positions for command block"""
            def noteDele(self, sender, beat, count, note, velocity):
                return Vec3(0, 0, 0)
        class CmdGen(RMG.DeleManager.NoteDele):
            """Generate commands set in command block"""
            def noteDele(self, sender, beat, count, note, velocity):
                return ""
        
        def __init__(self, pos = PosGen(), cmd = CmdGen()):
            self.pos = pos
            self.cmd = cmd

    def __init__(self, gen = GenManager()):
        self.gen = gen
    
    def noteDele(self, sender, beat, count, note, velocity):
        axis = sender.genInfo.axis
        pos = self.gen.pos.noteDele(self, beat, count, note, velocity)
        sender.mc.setBlockWithNBT(axis.Vec3L(pos), block.COMMAND_BLOCK, '',
            '{Command: "' +
                self.gen.cmd.noteDele(self, beat, count, note, velocity)
            + '"}'
        )

class CommonPosGen(SingleCB.GenManager.PosGen):
    """A position generator which suits common redstone music project"""
    def __init__(self,  unitBeat    = 1,
                        partPoses   = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 4),
                        unitDlt     = Vec3(0, 0, 3),
                        offset      = Vec3(0, 0, 2),
                        facing      = 1,
                        countPoses  = [Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1)]):
        """
        :param unitBeat: how many beats will a unit contain
        :param partPoses: for each part set a delta position (every beat is devided into len(partPoses) parts)
        :param unitDlt: delta movement per unit
        :param offset: global offset to Vec3L(0, 0, 0)
        :param facing: 1 = left, -1 = right, 0 = middle (special)
        :param countPoses: multiple delta positions for multiple notes on a same time point
        """
        self.unitBeat   = unitBeat
        self.partPoses  = partPoses
        self.unitDlt    = unitDlt
        self.offset     = offset
        self.facing     = facing
        self.countPoses = countPoses

    def noteDele(self, sender, beat, count, note, velocity):
        unitPart = len(self.partPoses)
        t = int(beat * unitPart)
        unit = floor(t / unitPart)
        div  = t % unitPart
        pos = self.offset + self.partPoses[div] * self.facing + self.unitDlt * unit + self.countPoses[count]
        return pos

class LkrbCmdGen(SingleCB.GenManager.CmdGen):
    def __init__(self, force = "fff"):
        self.force = force
    def noteDele(self, sender, beat, count, note, velocity):
        return '/execute @a ~ ~ ~ playsound lkrb.piano.p' + str(note) + self.force + ' record @p ~ ~ ~'