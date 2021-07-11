from .RMG import *
from myUtils.vecStepList import *

class UniversalRMG(RMG):
    def __init__(self, mc):
        super().__init__(mc)
        self.genInfo.info = {
                "unitBeat"  : 1,                                                # how many beats will a unit contain
                "partPoses" : vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 4),     # multiple delta positions for parts
                "unitDlt"   : Vec3(0, 0, 3),                                    # delta movement per unit
                "offset"    : Vec3(0, 1, 2),                                    # global offset to Vec3L(0, 0, 0)
                "facing"    : 1,                                                # 1 = left, -1 = right, 0 = middle(special)
                "countPoses": [Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1)],   # multiple delta positions for multiple notes on a same time point
                "force"     : "fff"
            }
    def noteTrigger(self, note, time, count):
        axis     = self.genInfo.axis
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
        # self.mc.postToChat()

        pos = offset + partPoses[div] * facing + unitDlt * unit + countPoses[count]

        self.mc.setBlockWithNBT(axis.Vec3L(pos), block.COMMAND_BLOCK, '', '{Command: "/execute @a ~ ~ ~ playsound lkrb.piano.p' + str(note) + force + ' record @p ~ ~ ~"}')
