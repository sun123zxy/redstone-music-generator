from myUtils.vecStepList import vecStepList
from mine import *
from myUtils.LocalAxis import *
from myUtils.direction import *
from RMG.UniversalRMG import UniversalRMG

mc = Minecraft()

rmg = UniversalRMG(mc)
rmg.loadMIDI("RMGTest/spark.mid")

rmg.genInfo.axis = getPlayerFwdAxis(mc)

rmg.genInfo.info['unitBeat'] = 1
rmg.genInfo.info['partPoses'] = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 8)
rmg.genInfo.info['unitDlt'] = Vec3(0, 0, 3)
rmg.genInfo.info['offset'] = Vec3(0, 0, 2)
rmg.genInfo.info['force'] = "fff"

rmg.genInfo.staBeat = 0 * 4
rmg.genInfo.endBeat = 4 * 4

rmg.genInfo.trackId = 1 + 1
rmg.genInfo.info['facing'] = 1
rmg.generate()

rmg.genInfo.trackId = 2 + 1
rmg.genInfo.info['facing'] = -1
rmg.generate()