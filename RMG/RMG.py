from mine import *
from myUtils import binarySearch
from myUtils.LocalAxis import *
from myUtils.direction import *
from myUtils.echo import *
from RMG.MIDIHandler import MIDIHandler

class RMG:
    """Redstone Music Generator"""
    
    class GenInfo:
        def __init__(self, axis, trackId, staBeat = 0, endBeat = int(1e18), info = {}):
            self.axis = axis
            self.trackId = trackId
            self.staBeat = staBeat # close left
            self.endBeat = endBeat # open right (interval)

    class NoteDele:
        def noteDele(self, sender, note, time, count):
            """Methods which recieve note infomation, should be overrided."""
            pass
    
    class BeatDele:
        def beatDele(self, sender, beat):
            """Methods which recieve beat infomation, should be overrided."""
            pass

    def __init__(self, mc, midi, noteTrigger, beatTrigger = BeatDele()):
        """
        :param midi: MIDIHandler
        :param noteTrigger: NoteDele
        :param beatTrigger: BeatDele
        """
        self.mc = mc
        self.midi = midi
        self.noteTrigger = noteTrigger
        self.beatTrigger = beatTrigger
        self.genInfo = RMG.GenInfo(
            axis = LocalAxis(self.mc, Vec3(0, 0, 0), Vec3(0, 0, 1)),
            trackId = 2
        )
        echo("RMG Initialized")
        
    def generate(self):
        echo("-----RMG Generate-----")
        echo("Initializing...")
        tId     = self.genInfo.trackId
        track   = self.midi.mid.tracks[tId]
        timeSav = self.midi.timeSav[tId]
        tpb     = self.midi.tpb

        mxBeat  = ceil(timeSav[len(timeSav) - 1] / tpb)
        staBeat = self.genInfo.staBeat
        endBeat = min(self.genInfo.endBeat, mxBeat)
        staPos  = binarySearch.firstRE(timeSav, staBeat * tpb)
        endPos  = binarySearch.lastL  (timeSav, endBeat * tpb)
        echo("Initialized")

        echo("Beat triggering ...")
        for i in range(staBeat, endBeat):
            self.beatTrigger.beatDele(self, i)
        echo("Beat triggering done")

        echo("Note triggering...")
        count = 0
        for i in range(staPos, endPos + 1):
            msg = track[i]
            if msg.time != 0:
                count = 0
            if msg.type == "note_on":
                self.noteTrigger.noteDele(self, msg.note, timeSav[i] - staBeat * tpb, count)
                count += 1
        echo("Note triggering done")
        echo("RMG generating done")
        echo("----------")
