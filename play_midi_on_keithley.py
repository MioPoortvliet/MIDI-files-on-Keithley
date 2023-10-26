import pretty_midi
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.adapters import VISAAdapter
from librosa import midi_to_hz
from datetime import datetime
from time import sleep
device_adres="COM43"
instrument = VISAAdapter(device_adres, timeout=500, read_termination='\r', write_termination='\r')
kl = Keithley2400(instrument)
#fname = 'Super_Mario_Bros_-_Warp_Pipe_Sound_Effect.mid' # Instrument: 0
#fname = 'running_in_90s.mid' # Instrument: 2
fname="smbt.mid" # Instrument: 0

def play_midi_on_keithley(fname, instrument_nr=0, device=kl):
    """Should edit this such that multi-voice is supported"""
    midi_data = pretty_midi.PrettyMIDI(fname)
    print("duration:",midi_data.get_end_time())
    print(f'{"note":>10} {"start":>10} {"end":>10}')
    start_time = datetime.now()
    current_note_end = 0
    print(midi_data.instruments)
    instrument = midi_data.instruments[instrument_nr]
    print("instrument:", instrument.program);
    for note in instrument.notes:
        print(note.pitch, note.start, note.end)
        note_hz = midi_to_hz(note.pitch)
        time_delta = datetime.now() - start_time
        if note.start >= current_note_end:
            sleep(note.start - current_note_end)
            #print(f"note_hz: {note_hz}")
            kl.beep(note_hz, note.end-note.start)
            sleep(note.end-note.start)
            current_note_end = note.end
                
if __name__ == "__main__":
    play_midi_on_keithley(fname)