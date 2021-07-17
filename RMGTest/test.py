from myUtils.vecStepList import vecStepList
from mine import *
from myUtils.LocalAxis import *
from myUtils.direction import *
from RMG.MIDIHandler import *
from RMG.RMG import *
from RMG.SingleCB import *
from myUtils import echo
from myUtils.echo import echo

mc = Minecraft()
echo.echo_mc = mc

midiHandler = MIDIHandler("RMGTest/spark.mid")
gen = SingleCB.GenManager(pos=CommonPosGen(), cmd=LkrbCmdGen())
dele = RMG.DeleManager(note=SingleCB(gen))
rmg = RMG(mc, midiHandler, dele)

gen.pos.unitBeat   = 1
gen.pos.partPoses  = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 8)
gen.pos.unitDlt    = Vec3(0, 0, 3)
gen.pos.offset     = Vec3(0, 0, 2)

gen.cmd.force = "fff"

rmg.genInfo.axis = getPlayerFwdAxis(mc)
rmg.genInfo.staBeat = 0 * 4
rmg.genInfo.endBeat = 8 * 4

rmg.genInfo.trackId = 1 + 1
gen.pos.facing = 1
rmg.generate()

rmg.genInfo.trackId = 2 + 1
gen.pos.facing = -1
rmg.generate()
