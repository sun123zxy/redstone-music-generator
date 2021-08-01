from fractions import Fraction
from mine import *
from myUtils import binarySearch
from myUtils.LocalAxis import *
from myUtils.direction import *
from myUtils.Event import *
from myUtils.echo import echo
from RMG.MIDIHandler import MIDIHandler

class RMG:
    """Redstone Music Generator"""
    def __init__(self, midiHan, noteEvent=Event(), beatEvent=Event()):
        """
        :param midiHan: MIDIHandler
        """
        self.midiHan = midiHan
        self.trackId = 2
        self.staBeat = 0 # close left
        self.endBeat = int(1e18) # open right (interval)
        self.noteEvent = noteEvent
        self.beatEvent = beatEvent
        echo("RMG Initialized")
        
    def generate(self):
        echo("-----RMG Generate-----")
        echo("Initializing...")
        tId     = self.trackId
        track   = self.midiHan.mido.tracks[tId]
        timeSav = self.midiHan.timeSav[tId]
        tpb     = self.midiHan.tpb

        mxBeat  = ceil(timeSav[len(timeSav) - 1] / tpb)
        staBeat = self.staBeat
        endBeat = min(self.endBeat, mxBeat)
        staPos  = binarySearch.firstRE(timeSav, staBeat * tpb)
        endPos  = binarySearch.lastL  (timeSav, endBeat * tpb)
        echo("Initialized")

        echo("Beat triggering ...")
        for i in range(staBeat, endBeat):
            self.beatEvent.on(sender=self, beat=i)
        echo("Beat triggering done")

        echo("Note triggering...")
        count = 0
        for i in range(staPos, endPos + 1):
            msg = track[i]
            if msg.time != 0:
                count = 0
            if msg.type == "note_on":
                self.noteEvent.on(sender=self, 
                                  beat=Fraction(timeSav[i] - staBeat * tpb, tpb),
                                  count=count,
                                  note=msg.note,
                                  velocity=msg.velocity)
                count += 1
        echo("Note triggering done")
        echo("RMG generating done")
        echo("----------")

class IMcAxis():
    def __init__(self, mc, axis = None):
        self.mc = mc
        if axis == None:
            self.axis = LocalAxis(mc, Vec3(0,0,0), Vec3(0,0,1))
        else:
            self.axis = axis