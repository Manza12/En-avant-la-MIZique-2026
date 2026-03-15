from pathlib import Path

from musictensors.audio import render_midi_to_audio
from musictensors.functions import concatenation
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument, Section
from musictensors.plot import plot_notes, plt
from musictensors import frac


# Tonic
D4 = Pitch(62)

# Octaves
octave_4 = D4
octave_3 = D4 - 12
octave_2 = D4 - 12 * 2
octave_5 = D4 + 12
octave_6 = D4 + 12 * 2

# Textures
t_1 = Texture(
    Rhythm(Hit('0', '1/2')),
    Rhythm(Hit('1/2', '1/4')),
    Rhythm(Hit('3/4', '1/4')),
)
t_1_bis = Texture(
    Rhythm(Hit('1/4', '1/4')),
    Rhythm(Hit('1/2', '1/4')),
    Rhythm(Hit('3/4', '1/4')),
)
t_2 = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('1/4', '1/4')),
    Rhythm(Hit('2/4', '1/4')),
    Rhythm(Hit('3/4', '1/4')),
)
t_2_bis = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('1/4', '1/4')),
    Rhythm(Hit('2/4', '1/4')),
    Rhythm(Hit('3/4', '1/2')),
)
t_3 = Texture(
    Rhythm(Hit('0', '3/8')),
    Rhythm(Hit('3/8', '1/8'), Hit('2/4', '1/2')),
)
t_4 = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('1/4', '1/8'), Hit('2/4', '1/4')),
    Rhythm(Hit('3/8', '1/8')),
    Rhythm(Hit('3/4', '1/4')),
)

# Orquestration
piano = Instrument('Acoustic Grand Piano')
s_piano = Section(piano)

# Harmony
## Tonal degrees
tonic = Chord({0})
supertonic = Chord({2})
mediant = Chord({4})
subdominant = Chord({5})
tritone = Chord({6})
dominant = Chord({7})
submediant = Chord({9})
leading_tone = Chord({11})

supertonic_ = supertonic + (-12)
mediant_ = mediant + (-12)
subdominant_ = subdominant + (-12)
tritone = tritone + (-12)
dominant_ = dominant + (-12)
submediant_ = submediant + (-12)
leading_tone_ = leading_tone + (-12)

# Phrases
## Phrase 1
t_ph_1 = t_1 - t_2 - t_1 - t_3
h_ph_1_head = Harmony(
    Chord(mediant),
    Chord(subdominant),
    Chord(dominant),
    Chord(dominant),
    Chord(subdominant),
    Chord(mediant),
    Chord(supertonic),
    Chord(tonic),
    Chord(supertonic),
    Chord(mediant)
)
h_ph_1_tail = Harmony(
    Chord(mediant),
    Chord(supertonic),
)
h_ph_1 = h_ph_1_head + h_ph_1_tail
h_ph_1 = octave_2 + (h_ph_1 | (h_ph_1 + 12))

phrase_1 = t_ph_1 * h_ph_1 * (s_piano * len(t_ph_1))

## Phrase 2
h_ph_2_tail = Harmony(
    Chord(supertonic),
    Chord(tonic),
)
h_ph_2 = h_ph_1_head + h_ph_2_tail
h_ph_2 = octave_2 + (h_ph_2 | (h_ph_2 + 12))
phrase_2 = t_ph_1 * h_ph_2 * (s_piano * len(t_ph_1))

## Phrase 3
t_ph_3 = t_1 - t_4 - t_4 - t_2_bis

h_ph_3_1 = Harmony(Chord(supertonic), Chord(mediant), Chord(tonic))
h_ph_3_2 = Harmony(Chord(supertonic), Chord(mediant), Chord(subdominant), Chord(tonic))
h_ph_3_3 = Harmony(Chord(supertonic), Chord(mediant), Chord(subdominant), Chord(supertonic))
h_ph_3_4 = Harmony(Chord(tonic), Chord(supertonic), Chord(dominant_), Chord(mediant))

h_ph_3 = h_ph_3_1 + h_ph_3_2 + h_ph_3_3 + h_ph_3_4
h_ph_3 = octave_2 + (h_ph_3 | (h_ph_3 + 12))

phrase_3 = t_ph_3 * h_ph_3 * (s_piano * len(t_ph_3))

## Phrase 4
t_ph_4 = t_1_bis - t_2 - t_1 - t_3

h_ph_3_1 = Harmony(Chord(supertonic), Chord(mediant), Chord(tonic))
h_ph_3_2 = Harmony(Chord(supertonic), Chord(mediant), Chord(subdominant), Chord(tonic))
h_ph_3_3 = Harmony(Chord(supertonic), Chord(mediant), Chord(subdominant), Chord(supertonic))
h_ph_3_4 = Harmony(Chord(tonic), Chord(supertonic), Chord(dominant_), Chord(mediant))

h_ph_4 = Harmony(
    Chord(mediant),
    Chord(subdominant),
    Chord(dominant),
    Chord(dominant),
    Chord(subdominant),
    Chord(mediant),
    Chord(supertonic),
    Chord(tonic),
    Chord(supertonic),
    Chord(mediant),
    Chord(supertonic),
    Chord(tonic),
)
h_ph_4 = octave_2 + (h_ph_4 | (h_ph_4 + 12))

phrase_4 = t_ph_4 * h_ph_4 * (s_piano * len(t_ph_4))


## Full piece
piece = concatenation(phrase_1, phrase_2, phrase_3, (phrase_4 + frac('-1/4')))

# Paths
name = 'ode_joie_melody'
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

# Write MIDI
midi = piece.to_midi(bpm=80*2, velocity=127)
midi.write(midi_path)

# Render MIDI to audio
sound_font = 'Arachno'

sound_fonts_paths = {
    'FluidR3_GM2-2': Path("../../../SoundFonts/FluidR3_GM2-2.sf2"),
    'GeneralUser': Path("../../../SoundFonts/GeneralUser-GS/GeneralUser-GS.sf2"),
    'Musyng Kite': Path("../../../SoundFonts/Musyng_Kite/Musyng_Kite.sf2"),
    'Arachno': Path("../../../SoundFonts/Arachno/Arachno-v1.0.sf2"),
}
sf2_path = sound_fonts_paths[sound_font]

render_midi_to_audio(
    midi_path,
    audio_path,
    sf2_path
)

# Plot
plot_notes(piece,
           figsize=(12, 6),
           x_tick_start=0,
           x_tick_step=1,)
plt.show()
