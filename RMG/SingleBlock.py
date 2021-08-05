from .RMG import *
from myUtils.vecStepList import *

class SingleBlock(IMcAxis):
    """for each note generate a single block with NBT."""

    def __init__(self, mc, axis, posDele=None, blockDele=None):
        """
        :param posDele: function return Vec3
        :param blockDele: function return (blockId, nbt)
        """
        super().__init__(mc, axis)
        self.posDele = posDele
        self.blockDele = blockDele

    def onNote(self, sender, beat, count, note, velocity):
        pos = self.posDele(sender=self,
                           beat=beat,
                           count=count,
                           note=note,
                           velocity=velocity)
        block, nbt = self.blockDele(sender=self,
                                    beat=beat,
                                    count=count,
                                    note=note,
                                    velocity=velocity)
        self.mc.setBlockWithNBT(self.axis.Vec3L(pos), block, '', nbt)

class AdvancingPosGen():
    """a position generator which suits advancing-styled redstone music project"""
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

class NoteBlockGen():
    """
    basic noteblock generator
    good old days
    """
    def genBlock(self, sender, beat, count, note, velocity):
        note = ((note - 54) % 24 + 24) % 24
        nbt = '{note: ' + str(note) + '}'
        return block.NOTEBLOCK, nbt
class LkrbBlockGen():
    """
    command block generator for realpiano
    (a sound resourcepack made by lkrb. see http://lkrb.net/blog/54.html for more information)
    """
    def __init__(self, force = "fff"):
        self.force = force
    def genBlock(self, sender, beat, count, note, velocity):
        nbt = '{Command: "/execute @a ~ ~ ~ playsound lkrb.piano.p' + str(note) + self.force + ' record @p ~ ~ ~"}'
        return block.COMMAND_BLOCK, nbt