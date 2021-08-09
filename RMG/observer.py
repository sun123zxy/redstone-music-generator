from fractions import Fraction
from mine import *
from .util.LocalAxis import *
from .util.direction import *
from .util.Event import *
from .util.echo import echo
from .util.vecStepList import *

class AdvancingPosGen():
    """a position generator which suits advancing-styled redstone music project"""
    @property
    def unitBeat(self):
        return self._unitBeat
    @unitBeat.setter
    def unitBeat(self, value):
        self._unitBeat = Fraction(value)

    def __init__(self,  unitBeat    = 1,
                        partPoses   = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 4),
                        unitDlt     = Vec3(0, 0, 3),
                        offset      = Vec3(0, 0, 2),
                        facing      = -1,
                        countPoses  = [Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1)]):
        """
        :param unitBeat: how many beats will a unit contain. Should be a fraction if needed.
        :param partPoses: for each part set a delta position (every beat is devided into len(partPoses) parts)
        :param unitDlt: delta movement per unit
        :param offset: global offset to Vec3L(0, 0, 0)
        :param facing: -1 = left, 1 = right, 0 = middle (special)
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
        tFrac = beat * unitPart / self.unitBeat
        if(tFrac.numerator % tFrac.denominator != 0): 
            echo("Error in class AdvancingPosGen function genPos(): \n"
               + "    cannot find a valid position to place the note. \n"
               + "    beat * unitPart / unitBeat is not an integer")
            exit()
        t = int(tFrac)
        unit = floor(t / unitPart)
        div  = t % unitPart
        pos = self.offset + self.partPoses[div] * self.facing + self.unitDlt * unit + self.countPoses[count]
        return pos
class AirBlockGen():
    """
    air block generator
    which means doing nothing lol
    """
    def genBlock(self, sender, beat, count, note, velocity):
        return block.AIR

class NoteBlockGen():
    """
    basic noteblock generator
    good old days
    """
    def genBlock(self, sender, beat, count, note, velocity):
        blk = block.NOTEBLOCK
        note = ((note - 54) % 24 + 24) % 24
        blk.nbt = '{note: ' + str(note) + '}'
        return blk

class LkrbBlockGen():
    """
    command block generator for realpiano
    (a sound resourcepack made by lkrb. see http://lkrb.net/blog/54.html for more information)
    """
    def __init__(self, force = "fff"):
        self.force = force
    def genBlock(self, sender, beat, count, note, velocity):
        blk = block.COMMAND_BLOCK
        blk.nbt = '{Command: "/execute @a ~ ~ ~ playsound lkrb.piano.p' + str(note) + self.force + ' record @p ~ ~ ~"}'
        return blk

# ------

class SingleBlock():
    """for each note generate a single block."""

    def __init__(self, mc, axis, posDele=None, blockDele=None):
        """
        :param posDele: a posGen() return Vec3
        :param blockDele: a blockGen() return Block
        """
        self.mc = mc
        self.axis = axis

        self.posDele = posDele
        self.blockDele = blockDele

    def onNote(self, sender, beat, count, note, velocity):
        pos = self.posDele(sender=self,
                           beat=beat,
                           count=count,
                           note=note,
                           velocity=velocity)
        block = self.blockDele(sender=self,
                               beat=beat,
                               count=count,
                               note=note,
                               velocity=velocity)
        self.mc.setBlockWithNBT(self.axis.Vec3L(pos), block)

class GroundedAdvancing():
    @property
    def mc(self):
        return self._singleBlock.mc
    @mc.setter
    def mc(self, value):
        self._singleBlock.mc = value
    @property
    def axis(self):
        return self._singleBlock.axis
    @axis.setter
    def axis(self, value):
        self._singleBlock.axis = value

    @property
    def unitBeat(self):
        return self._apg.unitBeat
    @unitBeat.setter
    def unitBeat(self, value):
        value = Fraction(value)
        if value.denominator == 1 or value.numerator == 1:
            self._apg.unitBeat = value
        else:
            echo("Error in class GroundAdvancing function unitBeat.setter(): \n"
               + "    failed to set unitBeat. one of the numerator and denominator must be 1.")
            exit()

    @property
    def unitPart(self):
        return len(self._apg.partPoses)
    @unitPart.setter
    def unitPart(self, value):
        self._apg.partPoses = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), value)

    @property
    def unitDltFwd(self):
        return self._apg.unitDlt.z
    @unitDltFwd.setter
    def unitDltFwd(self, value):
        self._apg.unitDlt = Vec3(0, 0, value)
        self._apg.offset = self.offset + Vec3(0, 0, value - 1)

    @property
    def offset(self):
        return self._offset
    @offset.setter
    def offset(self, value):
        self._offset = value
        self._apg.offset = value + Vec3(0, 0, self.unitDltFwd - 1)

    @property
    def facing(self):
        return self._apg.facing
    @facing.setter
    def facing(self, value):
        self._apg.facing = value

    @property
    def countPoses(self):
        return self._countPoses
    @countPoses.setter
    def countPoses(self, value):
        self._countPoses = self._apg.countPoses = value

    def __init__(self, mc, axis, blockDele, baseBlock = block.STONE,
                                            partBlock = block.DIRT,
                                            partDelay = 1,
                                            unitBeat    = 1,
                                            unitPart    = 4,
                                            unitDltFwd  = 3,
                                            offset      = Vec3(0, 0, 0),
                                            facing      = -1,
                                            countPoses  = [Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1)]):
        """
        :param blockDele: a blockGen() return Block
        :param baseBlock: block A used to constuct the ground
        :param partBlock: block B used to constuct the ground
        :param partDelay: delay redstone ticks (using repeater) between parts
        :param unitBeat: how many beats will a unit manage. Should be a fraction if needed.
        :param unitPart: how many parts will a unit contain.
        :param unitDltFwd: delta foward  movement per unit
        :param offset: global offset to Vec3L(0, 0, 0)
        :param facing: -1 = left, 1 = right, 0 = middle (special)
        :param countPoses: multiple delta positions for multiple notes on a same time point
        """
        self.blockDele = blockDele
        self.partDelay = partDelay
        self.baseBlock  = baseBlock
        self.partBlock  = partBlock

        self._apg = AdvancingPosGen()
        self._singleBlock = SingleBlock(mc, axis, self._apg.genPos, self.blockDele)
        self.unitBeat   = unitBeat
        self.unitPart   = unitPart

        self._unitDltFwd = 0
        self._offset = Vec3(0 ,0 ,0)
        self.unitDltFwd = unitDltFwd
        self.offset     = offset

        self.facing     = facing
        self.countPoses = countPoses

    def onNote(self, sender, beat, count, note, velocity):
        self._singleBlock.onNote(sender, beat, count, note, velocity)

    def onBeat(self, sender, beat):
        if self.unitBeat.denominator == 1:
            if beat % int(self.unitBeat) != 0:
                return
        ub = int(beat / self.unitBeat)
        for unit in range(ub, ub + self.unitBeat.denominator):
            origin = self._apg.offset + Vec3(0, 0, unit * self.unitDltFwd)
            # trunk
            cnt = self.unitPart * self.partDelay
            for i in range(1, self.unitDltFwd):
                pos = origin + Vec3(0, 0, -i)
                self.mc.setBlockWithNBT(self.axis.Vec3L(pos + Vec3(0,-1,0)), self.baseBlock)
                delay = min(cnt, 4)
                if delay != 0:
                    self.mc.setBlock(self.axis.Vec3L(pos),
                                     block.REDSTONE_REPEATER_INACTIVE.id,
                                     (delay - 1) * 4 + direction(-self.axis.fwd))
                    cnt -= delay
                else:
                    self.mc.setBlock(self.axis.Vec3L(pos), 55) # REDSTONE_WIRE
            # center
            self.mc.setBlockWithNBT(self.axis.Vec3L(origin + Vec3(0,-1,0)), self.baseBlock)
            self.mc.setBlock(self.axis.Vec3L(origin), 55) # REDSTONE_WIRE
            # ---
            dir = Vec3(self.facing, 0, 0)
            realDir = Vec3(0,0,0)
            if self.facing == -1:
                realDir = self.axis.left
            elif self.facing == 1:
                realDir = self.axis.right
            # bar sign
            if self.facing != 0:
                if unit == ub and beat % sender.midiHan.numerator == 0:
                    pos = origin + dir * (2 * self.unitPart + 1) + Vec3(0, 0, -1)
                    self.mc.setBlockWithNBT(self.axis.Vec3L(pos + Vec3(0,-1,0)), self.baseBlock)
                    self.mc.setBlockWithNBT(self.axis.Vec3L(pos + Vec3(0, 0,0)), self.baseBlock)
                    self.mc.setBlockWithNBT(self.axis.Vec3L(pos + Vec3(0, 1,0)), self.partBlock)
                if unit == ub + self.unitBeat.denominator - 1 and beat % sender.midiHan.numerator == 3:
                    pos = origin + dir * (2 * self.unitPart + 1) + Vec3(0, -1, 1)
                    self.mc.setBlockWithNBT(self.axis.Vec3L(pos), self.partBlock)
            # branch
            for i in range(0, self.unitPart):
                pos = origin + dir * i * 2
                self.mc.setBlockWithNBT(self.axis.Vec3L(pos + dir * 1 + Vec3(0,-1,0)), self.baseBlock)
                self.mc.setBlockWithNBT(self.axis.Vec3L(pos + dir * 2 + Vec3(0,-1,0)), self.baseBlock)
                self.mc.setBlockWithNBT(self.axis.Vec3L(pos + dir * 2 + Vec3(0, 0,0)), self.partBlock)
                if i == 0 and self.facing != 0:
                    self.mc.setBlock(self.axis.Vec3L(pos + dir * 1), 55) # REDSTONE_WIRE
                elif self.facing != 0:
                    self.mc.setBlock(self.axis.Vec3L(pos + dir * 1),
                                     block.REDSTONE_REPEATER_INACTIVE.id,
                                     (self.partDelay - 1) * 4 + direction(-realDir))
            if cnt != 0:
                echo("Error in class GroundedAdvancing function onBeat(): \n"
                   + "    at beat " + str(beat) + " (unit " + str(unit) + ") \n"
                   + "    unitDltFwd is not enough to place repeaters between units")
                exit()

class GroundedSnake():
    pass

class FallingPianoRoll():
    pass