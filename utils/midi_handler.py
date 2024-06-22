import math
from fractions import Fraction

import mido


class MIDIHandler():
    def __init__(self, file_path:str) -> None:
        print(">>> MIDIHandler >>>")
        print("Analyzing " + file_path + " ...")
        self.mid = mido.MidiFile(file_path)
        self.num = self.deno = self.tempo = self.bpm = None
        self.tpb = self.mid.ticks_per_beat
        mx_time = [None] * len(self.mid.tracks)
        for i, track in enumerate(self.mid.tracks):
            print("Track {}: {}".format(i, track.name))
            cnt = 0
            timer = 0
            for msg in track:
                timer += msg.time
                if(msg.is_meta):
                    if(cnt > 0):
                        print("    " + str(cnt) + " musicial messages omitted")
                        cnt = 0
                    print("    " + str(msg))
                    if msg.type == "time_signature":
                        self.num = msg.numerator
                        self.deno = msg.denominator
                    elif msg.type == "set_tempo":
                        self.tempo = msg.tempo
                        self.bpm = mido.tempo2bpm(self.tempo)
                else:
                    cnt += 1
            if(cnt > 0):
                print("    " + str(cnt) + " musicial messages omitted")
            mx_time[i] = timer
        self.mx_beat = [Fraction(time, self.tpb) for time in mx_time]
        print("Analysis done")
        print("numerator/denominator: " + str(self.num) + "/" + str(self.deno))
        print("tempo(bpm): " + str(self.tempo) + "(" + str(self.bpm) + ")")
        print("ticks per beat: " + str(self.tpb))
        print("max beat: " + str(self.mx_beat))
        print("<<< MIDIHandler <<<")
    
    def msg_gen(self, config: dict):
        """[st_beat, ed_beat)"""

        track: int = config.get("track")
        st_beat: Fraction = config.get("st_beat")
        ed_beat: Fraction = config.get("ed_beat")
        type_switch: dict = config.get("type_switch")

        def check(beat):
            return (True if st_beat == None else beat >= st_beat) and (True if ed_beat == None else beat < ed_beat)

        timer = 0
        lst = []
        programs = [None] * 16

        def _flush(timer):
            beat = Fraction(timer, self.tpb)
            my_beat = beat - (0 if st_beat == None else st_beat)
            if check(beat) and len(lst) > 0:
                return my_beat, lst
            

        for msg in self.mid.tracks[track]:
            if msg.time != 0:
                # >>> Same
                beat = Fraction(timer, self.tpb)
                my_beat = beat - (0 if st_beat == None else st_beat)
                if check(beat) and len(lst) > 0:
                    yield my_beat, lst
                lst = []
                # <<<
            timer += msg.time
            if msg.type == "program_change":
                programs[msg.channel] = msg.program
            if type_switch.get(msg.type) == True:
                lst.append((msg.type, msg.note, msg.velocity, programs[msg.channel]))
        # >>> Same
        beat = Fraction(timer, self.tpb)
        my_beat = beat - (0 if st_beat == None else st_beat)
        if check(beat) and len(lst) > 0:
            yield my_beat, lst
        lst = []
        # <<<
            

if __name__ == "__main__":
    midihan = MIDIHandler("my_script/spark.mid")
    config = {
        "track": 3,
        "st_beat": 3,
        "ed_beat": 4,
        "type_switch":{
            "note_on": True,
            "note_off": True
        }
    }
    for beat, lst in midihan.msg_gen(config):
        print(str(math.floor(beat)) + "+" + str(beat - math.floor(beat)))
        for msg in lst:
            print("    " + str(msg))