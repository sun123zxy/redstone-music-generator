from .RMG import *
from myUtils.vecStepList import *

class SingleCB(IMcAxis):
    """generate single command block for a note."""

    def __init__(self, mc, axis, posDele=None, cmdDele=None):
        """
        :param posDele: function
        :param cmdDele: function
        """
        super().__init__(mc, axis)
        self.posDele = posDele
        self.cmdDele = cmdDele

    def onNote(self, sender, beat, count, note, velocity):
        pos = self.posDele(sender=self,
                           beat=beat,
                           count=count,
                           note=note,
                           velocity=velocity)
        self.mc.setBlockWithNBT(self.axis.Vec3L(pos), block.COMMAND_BLOCK, '',
            '{Command: "' +
                self.cmdDele(sender=self,
                             beat=beat,
                             count=count,
                             note=note,
                             velocity=velocity)
            + '"}'
        )

class AdvancingPosGen():
    """A position generator which suits advancing-structured redstone music project"""
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
    def genPos(self, sender, beat, count, note, velocity):
        unitPart = len(self.partPoses)
        t = int(beat * unitPart)
        unit = floor(t / unitPart)
        div  = t % unitPart
        pos = self.offset + self.partPoses[div] * self.facing + self.unitDlt * unit + self.countPoses[count]
        return pos

class LkrbCmdGen():
    def __init__(self, force = "fff"):
        self.force = force
    def genCmd(self, sender, beat, count, note, velocity):
        return '/execute @a ~ ~ ~ playsound lkrb.piano.p' + str(note) + self.force + ' record @p ~ ~ ~'