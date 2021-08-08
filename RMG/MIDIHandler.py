import mido
from .util.echo import echo

class MIDIHandler:
    @property
    def mido(self):
        return self._mido
    @property
    def numerator(self):
        return self.mido.tracks[0][0].numerator
    @property
    def denominator(self):
        return self.mido.tracks[0][0].denominator
    @property
    def bpm(self):
        return mido.bpm2tempo(self.mido.tracks[1][0].tempo)
    @property
    def tpb(self):
        return self.mido.ticks_per_beat
    @property
    def timeSav(self):
        return self._timeSav
    @property
    def mxTime(self):
        return self._mxTime
    def __init__(self, midiPath):
        echo("-----MIDIHandler-----")
        echo("loading " + midiPath + " ...")
        self._mido = mido.MidiFile(midiPath)
        echo("numerator/denominator: " + str(self.numerator) + "/" + str(self.denominator))
        echo("BPM: " + str(self.bpm))
        echo("ticks per beat: " + str(self.tpb))

        self._timeSav = [[]] * len(self.mido.tracks) # save each note's time in each tracks
        self._mxTime = 0
        for i, track in enumerate(self.mido.tracks):
            echo('Track {}: {}'.format(i, track.name))
            self.timeSav[i] = [0] * len(track)
            timer = 0
            for j, msg in enumerate(track):
                timer += msg.time
                self.timeSav[i][j] = timer # prefix sum
                if i <= 1:
                    echo("    " + str(msg)) # output metaMassages
            self._mxTime = max(self._mxTime, timer)

        echo("max time: " + str(self._mxTime))

        echo(midiPath + " sucessfully loaded")
        echo("----------")