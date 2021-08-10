import mido
from .util.echo import echo

class MIDIHandler:
    @property
    def mido(self):
        return self._mido
    @property
    def numerator(self):
        return self._numerator
    @property
    def denominator(self):
        return self._denominator
    @property
    def tempo(self):
        return self._tempo
    @property
    def bpm(self):
        return mido.tempo2bpm(self._tempo)
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
        echo("analyzing " + midiPath + " ...")
        self._mido = mido.MidiFile(midiPath)
        self._timeSav = [[]] * len(self.mido.tracks) # save each note's time in each tracks
        self._numerator = None
        self._denominator = None
        self._tempo = None
        self._mxTime = 0
        for i, track in enumerate(self.mido.tracks):
            echo('Track {}: '.format(i))
            self.timeSav[i] = [0] * len(track)
            timer = 0
            count = 0
            for j, msg in enumerate(track):
                timer += msg.time
                self.timeSav[i][j] = timer # prefix sum
                if msg.is_meta:
                    if count != 0:
                        echo("    " + str(count) + " musicial messages omitted")
                        count = 0
                    echo("    " + str(msg)) # output metaMassages
                    if msg.type == "time_signature":
                        if self._numerator == None or (self._numerator == msg.numerator and self._denominator == msg.denominator):
                            self._numerator = msg.numerator
                            self._denominator = msg.denominator
                        else:
                            self._numerator = self._denominator = -1 # multiple n & d
                    elif msg.type == "set_tempo":
                        if self._tempo == None or self._tempo == msg.tempo:
                            self._tempo = msg.tempo
                        else:
                            self._tempo = -1 # multiple tempo
                else:
                    count = count + 1
            if count != 0:
                echo("    " + str(count) + " musicial messages omitted")
                count = 0
            self._mxTime = max(self._mxTime, timer)
        echo("")
        echo("numerator/denominator: " + str(self.numerator) + "/" + str(self.denominator))
        echo("tempo(bpm): " + str(self.tempo) + "(" + str(self.bpm) + ")")
        echo("ticks per beat: " + str(self.tpb))
        echo("max time: " + str(self._mxTime))
        echo(midiPath + " sucessfully loaded")
        echo("----------")