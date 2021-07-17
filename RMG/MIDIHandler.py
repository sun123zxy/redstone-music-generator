import mido
from myUtils.echo import echo

class MIDIHandler:
    def __init__(self, midiPath):
        echo("-----MIDIHandler-----")
        echo("Loading " + midiPath + " ...")
        self.mid = mido.MidiFile(midiPath)
        self.bpm = mido.bpm2tempo(self.mid.tracks[1][0].tempo)
        echo("BPM: " + str(self.bpm))
        self.tpb = self.mid.ticks_per_beat
        echo("Ticks per beat: " + str(self.tpb))

        self.timeSav = [[]] * len(self.mid.tracks) # save each note's time in each tracks
        for i, track in enumerate(self.mid.tracks):
            echo('Track {}: {}'.format(i, track.name))
            self.timeSav[i] = [0] * len(track)
            timer = 0
            for j, msg in enumerate(track):
                timer += msg.time
                self.timeSav[i][j] = timer
                if i <= 1:
                    echo("    " + str(msg)) # output metaMassages

        echo(midiPath + " sucessfully loaded")
        echo("----------")