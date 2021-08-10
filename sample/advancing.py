"""
sample script: advancing-styled redstone music, note only
choose command block (lkrb realpiano resourcepack) or noteblock
choose sample configurations
"""
from RMG.util.vecStepList import vecStepList
from mine import *
from RMG.util.LocalAxis import *
from RMG.util.direction import *
from RMG.MIDIHandler import *
from RMG.RMG import *
from RMG.observer import *
from RMG.util import echo
from RMG.util.echo import echo

mc = Minecraft()
echo.echo_mc = mc
axis = getPlayerFwdAxis(mc)

# ---Binding Plugins for RMG---
pos = AdvancingPosGen()

# CHOOSE COMMAND BLOCK OR NOTEBLOCK HERE
cmd = LkrbBlockGen()
# cmd = NoteBlockGen()

singleBlock = SingleBlock(mc, axis, pos.genPos, cmd.genBlock)
rmg = RMG(MIDIHandler("sample/spark.mid"))
rmg.noteEvent.append(singleBlock.onNote)

# ---Configuring---
pos.countPoses  = [Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1)]
pos.magnet = False
cmd.force = "fff"
# CHOOSE A SAMPLE CONFIGURATION
pos.unitBeat   = 1
pos.partPoses  = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 8)
pos.unitDlt    = Vec3(0, 0, 3)
pos.offset     = Vec3(0, 0, 2)
"""
pos.unitBeat   = Fraction(3,2)
pos.partPoses  = vecStepList(Vec3(2, 0, 0), Vec3(2, 0, 0), 12)
pos.unitDlt    = Vec3(0, 0, 4)
pos.offset     = Vec3(0, 0, 3)
"""

# ---Generating---

rmg.staBeat = 0 * 4
rmg.endBeat = 7 * 4

rmg.trackId = 1 + 1
pos.facing = -1
rmg.generate()

rmg.trackId = 2 + 1
pos.facing = 1
rmg.generate()