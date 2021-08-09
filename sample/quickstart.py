"""
sample script: using minimized code to do a quickstart
"""
from mine import *
from RMG.util.vecStepList import vecStepList
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
cmd = NoteBlockGen()
gadv = GroundedAdvancing(mc, axis, cmd.genBlock)
rmg = RMG(MIDIHandler("sample/spark.mid"))
rmg.noteEvent.append(gadv.onNote)
rmg.beatEvent.append(gadv.onBeat)

# ---Configuring---
gadv.unitPart = 8

# ---Generating---
rmg.trackId = 1 + 1
gadv.facing = -1
rmg.generate()
rmg.trackId = 2 + 1
gadv.facing = 1
rmg.generate()