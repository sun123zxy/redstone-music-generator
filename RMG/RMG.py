from fractions import Fraction
from mine import *
from .util import binarySearch
from .util.LocalAxis import *
from .util.direction import *
from .util.Event import *
from .util.echo import echo
from RMG.MIDIHandler import MIDIHandler

class RMG:
    """Redstone Music Generator"""
    def __init__(self, midiHan, noteEvent=Event(), beatEvent=Event()):
        """
        :param midiHan: MIDIHandler
        """
        self.midiHan = midiHan
        self.trackId = 2
        self.staBeat = 0 
        self.endBeat = ceil(self.midiHan.mxTime / self.midiHan.tpb) 

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
        staBeat = self.staBeat
        endBeat = self.endBeat
        staPos  = binarySearch.firstRE(timeSav, staBeat * tpb) # close left
        endPos  = binarySearch.lastL  (timeSav, endBeat * tpb) # open right (interval)
        echo("configure loaded: generate track " + str(tId) 
           + " from beat " + str(staBeat) + "(#" + str(staPos) + ")" + " to beat " + str(endBeat) + "(#" + str(endPos) + ")")
        echo("Initialized")
        
        echo("Beat triggering ...")
        for i in range(staBeat - staBeat, endBeat - staBeat):
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