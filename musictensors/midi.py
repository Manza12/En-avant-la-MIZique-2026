def to_midi(notes, velocity=64, bpm=100):
    import pretty_midi
    notes = notes
    start = min(note.onset for note in notes)
    midi = pretty_midi.PrettyMIDI()

    instruments = set(note.instrument for note in notes)
    for instrument in instruments:
        instrument_program = pretty_midi.instrument_name_to_program(instrument.name)
        track = pretty_midi.Instrument(program=instrument_program)
        notes_instrument = [note for note in notes if note.instrument == instrument]
        for note in notes_instrument:
            onset_s = float((note.onset - start) * 240 / bpm)
            duration_s = float(note.duration * 240 / bpm)
            end_s = onset_s + duration_s
            note = pretty_midi.Note(velocity=velocity, pitch=note.pitch.number, start=onset_s, end=end_s)
            track.notes.append(note)
        midi.instruments.append(track)
    return midi
