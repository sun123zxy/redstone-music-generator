from .RMG import *
from myUtils.vecStepList import *

class UniversalNoteTrigger(RMG.NoteDele):
    """Universal NoteTrigger for common redstone music project."""

    class PosManager(RMG.NoteDele):
        """Generate positions for command block"""
        def noteDele(self, sender, note, time, count):
            return Vec3(0, 0, 0)
    class CmdManager(RMG.NoteDele):
        """Generate commands set in command block"""
        def noteDele(self, sender, note, time, count):
            return ""

    def __init__(self, posMan = PosManager(), cmdMan = CmdManager()):
        self.posMan = posMan # position manager of command block
        self.cmdMan = cmdMan # command manager of command block
    
    def noteDele(self, sender, note, time, count):
        axis = sender.genInfo.axis
        pos = self.posMan.noteDele(self, note, time, count)
        sender.mc.setBlockWithNBT(axis.Vec3L(pos), block.COMMAND_BLOCK, '',
            '{Command: "' + self.cmdMan.noteDele(self, note, time, count) + '"}')

'''
        self.genInfo.info = {
                "unitBeat"  : 1,                                                # how many beats will a unit contain
                "partPoses" : vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 4),     # multiple delta positions for parts
                "unitDlt"   : Vec3(0, 0, 3),                                    # delta movement per unit
                "offset"    : Vec3(0, 1, 2),                                    # global offset to Vec3L(0, 0, 0)
                "facing"    : 1,                                                # 1 = left, -1 = right, 0 = middle(special)
                "countPoses": [Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1)],   # multiple delta positions for multiple notes on a same time point
                "force"     : "fff"
            }
'''
"""
        unitBeat = self.genInfo.info['unitBeat']
        partPoses= self.genInfo.info['partPoses']
        unitPart = len(partPoses)
        unitDlt  = self.genInfo.info['unitDlt']
        offset   = self.genInfo.info['offset']
        facing   = self.genInfo.info['facing']
        countPoses  = self.genInfo.info['countPoses']
        force    = self.genInfo.info['force']
        
        t = round(time * unitPart / unitBeat / self.tpb)
        unit = floor(t / unitPart)
        div  = t % unitPart
        # echo(str(unit) + ", " + str(div) + ": " + str(note))
"""

 # /execute @a ~ ~ ~ playsound lkrb.piano.p' + str(note) + force + ' record @p ~ ~ ~
 # pos = offset + partPoses[div] * facing + unitDlt * unit + countPoses[count]