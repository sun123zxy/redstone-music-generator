import mido
from mine import *
from myUtils import binarySearch
from myUtils.LocalAxis import *
from myUtils.direction import *

class RMGGenInfo:
    """RMG.generate() will use this"""
    def __init__(self, axis, trackId, staBeat = 0, endBeat = int(1e18), info = {}):
        self.axis = axis
        self.trackId = trackId
        self.staBeat = staBeat
        self.endBeat = endBeat  # not included
        self.info = info        # extra infomations
            
class RMG:
    """Redstone Music Generator"""
    
    def __init__(self, mc):
        self.mc = mc
        self.genInfo = RMGGenInfo(
            axis = LocalAxis(self.mc, Vec3(0, 0, 0), Vec3(0, 0, 1)),
            trackId = 2,
        )
        self.mid = None
        self.mc.postToChat("RMG Initialized")
    
    def loadMIDI(self, midiPath):
        self.mc.postToChat("Loading " + midiPath + " ...")
        self.mid = mido.MidiFile(midiPath)
        self.bpm = mido.bpm2tempo(self.mid.tracks[1][0].tempo)
        self.mc.postToChat("BPM: " + str(self.bpm))
        self.tpb = self.mid.ticks_per_beat
        self.mc.postToChat("Ticks per beat: " + str(self.tpb))

        self.timeSav = [[]] * len(self.mid.tracks) # save each note's time in each tracks
        for i, track in enumerate(self.mid.tracks):
            self.mc.postToChat('Track {}: {}'.format(i, track.name))
            self.timeSav[i] = [0] * len(track)
            timer = 0
            for j, msg in enumerate(track):
                timer += msg.time
                self.timeSav[i][j] = timer
                if i <= 1: self.mc.postToChat("    " + str(msg)) # output metaMassages

        self.mc.postToChat(midiPath + " sucessfully loaded")
        
    def generate(self):
        if self.mid == None:
            return
        tId     = self.genInfo.trackId
        mxBeat  = ceil(self.timeSav[tId][len(self.timeSav[tId]) - 1] / self.tpb)
        staBeat = self.genInfo.staBeat
        endBeat = min(self.genInfo.endBeat, mxBeat)
        staPos = binarySearch.firstRE(self.timeSav[tId], staBeat * self.tpb)
        endPos = binarySearch.lastL  (self.timeSav[tId], endBeat * self.tpb)
        track = self.mid.tracks[tId]
        
        for i in range(staBeat, endBeat):
            self.beatTrigger(i)

        count = 0
        for i in range(staPos, endPos + 1):
            msg = track[i]
            if msg.time != 0: count = 0
            if msg.type == "note_on":
                self.noteTrigger(msg.note, self.timeSav[tId][i] - staBeat * self.tpb, count)
                count += 1
        self.mc.postToChat("Generated!")
    
    def beatTrigger(self, beat):
        """Do some extra things. It should be overrided by childs."""
        pass
    def noteTrigger(self, note, time, count):
        """Defines how to generate command blocks(note). It should be overrided by childs."""
        pass
