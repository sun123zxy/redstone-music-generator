from .RMG import *

class UniversalRMG(RMG):
    def __init__(self, mc):
        super().__init__(mc)
        self.genInfo.info = {
                "unitBeat"  : 1,              # how many beats will a unit contain
                "unitDiv"   : 4,              # how many part will a unit be divided into
                "unitDlt"   : Vec3(0, 0, 3),  # delta position
                "offset"    : Vec3(0, 1, 2),  # start point
                "facing"    : 1,              # 1 = L, -1 = R, 0 = Middle(special)
                "countDlt"  : [Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1)],   # for multi notes on single time point
                "force"     : "fff"
            }
    def noteTrigger(self, note, time, count):
        axis    = self.genInfo.axis
        unitBeat= self.genInfo.info['unitBeat']
        unitDiv = self.genInfo.info['unitDiv']
        unitDlt = self.genInfo.info['unitDlt']
        offset  = self.genInfo.info['offset']
        facing  = self.genInfo.info['facing']
        countDlt= self.genInfo.info['countDlt']
        force   = self.genInfo.info['force']
        
        t = round(time * unitDiv / unitBeat / self.tpb)
        unit = floor(t / unitDiv)
        div  = t % unitDiv
        # self.mc.postToChat()

        pos = offset + Vec3(facing * 2 * (div + 1), 0, 0) + unitDlt * unit + countDlt[count]

        self.mc.setBlockWithNBT(axis.Vec3L(pos), block.COMMAND_BLOCK, '', '{Command: "/execute @a ~ ~ ~ playsound lkrb.piano.p' + str(note) + force + ' record @p ~ ~ ~"}')
