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
axis = getPlayerFwdAxis(mc)
# ---Binding Plugins for RMG---
pos = AdvancingPosGen(); cmd = LkrbCmdGen()
singleCB = SingleCB(mc, axis, pos.genPos, cmd.genCmd)
rmg = RMG(MIDIHandler("sample/spark.mid"))
rmg.noteEvent.append(singleCB.onNote)
# ---Config & Generating---
pos.unitBeat   = 1
pos.partPoses  = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 8)
pos.unitDlt    = Vec3(0, 0, 3)
pos.offset     = Vec3(0, 0, 2)

cmd.force = "fff"

rmg.staBeat = 0 * 4
rmg.endBeat = 8 * 4

rmg.trackId = 1 + 1
pos.facing = 1
rmg.generate()

rmg.trackId = 2 + 1
pos.facing = -1
rmg.generate()