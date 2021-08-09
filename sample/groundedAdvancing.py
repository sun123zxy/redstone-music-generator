"""
sample script: grounded advancing-styled redstone music
choose command block (lkrb realpiano resourcepack) or noteblock or ground only
choose sample configurations
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

# CHOOSE COMMAND BLOCK OR NOTEBLOCK OR GROUND ONLY (AIR)
cmd = LkrbBlockGen()
# cmd = NoteBlockGen()
# cmd = AirBlockGen()

gadv = GroundedAdvancing(mc, axis, cmd.genBlock)
rmg = RMG(MIDIHandler("sample/spark.mid"))
rmg.noteEvent.append(gadv.onNote)
rmg.beatEvent.append(gadv.onBeat)

# ---Configuring---
gadv.baseBlock = block.STONE
gadv.partBlock = block.REDSTONE_LAMP_INACTIVE

gadv.offset = Vec3(0,0,0)
gadv.countPoses = [Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1)]

cmd.force = "fff" # not needed if cmd is not LkrbBlockGen 

# CHOOSE A CONFIGURATION
gadv.partDelay = 1
gadv.unitBeat = 1
gadv.unitPart = 8
gadv.unitDltFwd = 3
"""
gadv.partDelay = 1
gadv.unitBeat = 2
gadv.unitPart = 16
gadv.unitDltFwd = 5
"""
"""
gadv.partDelay = 1
gadv.unitBeat = Fraction(1,2)
gadv.unitPart = 4
gadv.unitDltFwd = 3
"""
"""
gadv.partDelay = 1
gadv.unitBeat = Fraction(1, 3)
gadv.unitPart = 8
gadv.unitDltFwd = 3
"""
"""
gadv.partDelay = 2
gadv.unitBeat = 1
gadv.unitPart = 8
gadv.unitDltFwd = 5
"""
# A SPECIAL CONFIGURATION
"""
# a special configuration for facing=0 generating, check generating part below
gadv.partDelay = 1
gadv.unitBeat = Fraction(1, 8)
gadv.unitPart = 1
gadv.unitDltFwd = 2
gadv.countPoses = [Vec3(0, 1, 0), Vec3(-1, 0, 0), Vec3(1, 0, 0)]
"""
# SOME ERROR CONFIGURATION SAMPLES
"""
# an error configuration
# may be supported in the future
# gadv.partDelay = 1
# gadv.unitBeat = Fraction(3, 2)
# gadv.unitPart = 12
# gadv.unitDltFwd = 4
"""
"""
# an error configuration
# gadv.partDelay = 1
# gadv.unitBeat = 1
# gadv.unitPart = 4
# gadv.unitDltFwd = 3
"""
"""
# an error configuration
# gadv.partDelay = 1
# gadv.unitBeat = 1
# gadv.unitPart = 8
# gadv.unitDltFwd = 2
"""

# ---Generating---
rmg.staBeat = 0 * 4
rmg.endBeat = 7 * 4

# CHOOSE NORMAL OR FACING=0
# NORMAL
rmg.trackId = 1 + 1
gadv.facing = -1
rmg.generate()
rmg.trackId = 2 + 1
gadv.facing = 1
rmg.generate()
"""
# facing=0, use the special configuration above
rmg.trackId = 1 + 1
gadv.facing = 0
rmg.generate()
"""