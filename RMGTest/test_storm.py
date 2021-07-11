from mine import *
from LocalAxis import *
from direction import *
from RMG.UniversalRMG import UniversalRMG

mc = Minecraft()

rmg = UniversalRMG(mc)
rmg.loadMIDI("RMGTest/The Storm.mid")

rmg.genInfo.axis = getPlayerFwdAxis(mc)


rmg.genInfo.info['unitBeat']    = 1
rmg.genInfo.info['unitDiv']     = 4
rmg.genInfo.info['unitDlt']     = Vec3(0, 0, 2)
rmg.genInfo.info['offset']      = Vec3(0, 0, 1)
rmg.genInfo.staBeat = 0 * 4
rmg.genInfo.endBeat = 4 * 4

rmg.genInfo.trackId = 2 + 1
rmg.genInfo.info['facing'] = 1
rmg.generate()

rmg.genInfo.trackId = 4 + 1
rmg.genInfo.info['facing'] = -1
rmg.generate()


"""
rmg.genInfo.info['unitBeat']    = 1 / 2
rmg.genInfo.info['unitDiv']     = 2
rmg.genInfo.info['unitDlt']     = Vec3(0, 0, 2)
rmg.genInfo.info['offset']      = Vec3(0, 0, 1)
rmg.genInfo.staBeat = 40 * 4
rmg.genInfo.endBeat = 44 * 4

rmg.genInfo.trackId = 2 + 1
rmg.genInfo.info['facing'] = 1
rmg.generate()

rmg.genInfo.trackId = 6 + 1
rmg.genInfo.info['facing'] = -1
rmg.generate()
"""