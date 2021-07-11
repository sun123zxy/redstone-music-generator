from myUtils.vecStepList import vecStepList
from mine import *
from myUtils.LocalAxis import *
from myUtils.direction import *
from RMG.MIDIHandler import *
from RMG.RMG import *
from RMG.RMGDeles import *

mc = Minecraft()

rmg = RMG(mc, MIDIHandler("RMGTest/spark.mid"), UniversalNoteTrigger())

rmg.genInfo.axis = getPlayerFwdAxis(mc)
"""
rmg.genInfo.info['unitBeat'] = 1
rmg.genInfo.info['partPoses'] = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 8)
rmg.genInfo.info['unitDlt'] = Vec3(0, 0, 3)
rmg.genInfo.info['offset'] = Vec3(0, 0, 2)
rmg.genInfo.info['force'] = "fff"
"""
rmg.genInfo.staBeat = 0 * 4
rmg.genInfo.endBeat = 8 * 4


rmg.genInfo.trackId = 1 + 1
# rmg.genInfo.info['facing'] = 1
rmg.generate()


rmg.genInfo.trackId = 2 + 1
# rmg.genInfo.info['facing'] = -1
rmg.generate()
