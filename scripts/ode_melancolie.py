from pathlib import Path

from musictensors.audio import render_midi_to_audio
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

octave_melodie = octave_5

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

t_acc_head = Texture(
    Rhythm(Hit('0', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
    Rhythm(Hit('2/8', '1/8'))
)
t_acc_tail = Texture(
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
    Rhythm(Hit('0', '1/8'), Hit('2/8', '1/8')),
)
t_acc = Texture(
    Rhythm(Hit('0', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8'), Hit('5/8', '1/8'), Hit('7/8', '1/8')),
    Rhythm(Hit('2/8', '1/8'), Hit('4/8', '1/8'), Hit('6/8', '1/8')),
)
# t_acc_head = Texture(
#     Rhythm(Hit('0', '1/2')),
#     Rhythm(Hit('0', '1/2')),
#     Rhythm(Hit('0', '1/2')),
# )
# t_acc_tail = Texture(
#     Rhythm(Hit('0', '1/2')),
#     Rhythm(Hit('0', '1/2')),
# )
# t_acc = Texture(
#     Rhythm(Hit('0', '1')),
#     Rhythm(Hit('0', '1')),
#     Rhythm(Hit('0', '1')),
# )

# Orquestration
# s_melody_treb = Section(Instrument('Flute'))
s_melody_medi = Section(Instrument('Oboe'), Instrument('Flute'))
s_accompaniment = Section(Instrument('String Ensemble 1'))

# Harmony
## Tonal degrees
tonic = Chord({0})
supertonic = Chord({2})
mediant = Chord({3})
subdominant = Chord({5})
tritone = Chord({6})
dominant = Chord({7})
submediant = Chord({8})
superdominant = Chord({9})
subtonic = Chord({10})
leading_tone = Chord({11})

supertonic_ = supertonic + (-12)
mediant_ = mediant + (-12)
subdominant_ = subdominant + (-12)
tritone = tritone + (-12)
dominant_ = dominant + (-12)
submediant_ = submediant + (-12)
superdominant_ = superdominant + (-12)
subtonic_ = subtonic + (-12)
leading_tone_ = leading_tone + (-12)

# Phrases
## Phrase 1
### Melody
t_ph_1 = t_1 * t_2 * t_1 * t_3
h_ph_1_head = Harmony(
    mediant | dominant,
    subdominant | submediant,
    dominant | subtonic,
    dominant | subtonic,
    subdominant | submediant,
    mediant | dominant,
    supertonic | subdominant,
    tonic | mediant,
    supertonic | subdominant,
    mediant | dominant,
)
h_ph_1_tail = Harmony(
    mediant | dominant,
    supertonic | subdominant,
)
h_ph_1 = h_ph_1_head + h_ph_1_tail
h_ph_1 = octave_melodie + h_ph_1

phrase_1_mel_medi = t_ph_1 @ h_ph_1 @ (s_melody_medi * len(t_ph_1))
phrase_1_mel_treb = t_ph_1 @ (h_ph_1 + 12) @ (s_melody_medi * len(t_ph_1))
phrase_1_mel = phrase_1_mel_medi  # parallelization(phrase_1_mel_treb, phrase_1_mel_medi)

### Accompaniment
h_acc_I = octave_4 + Harmony(tonic | dominant, mediant | (tonic + 12), dominant | (mediant + 12))
h_acc_V = octave_4 + Harmony(dominant_ | subdominant, supertonic | leading_tone, subdominant | (supertonic + 12))
h_acc_VI = octave_4 + Harmony(submediant_ | mediant, tonic | dominant, mediant | (tonic + 12))
h_acc_I_bis = octave_4 + Harmony(mediant | (tonic + 12), dominant | (mediant + 12))
h_acc_I46 = octave_4 + Harmony(dominant_ | mediant, tonic | dominant, mediant | (tonic + 12))
h_acc_V_bis = octave_4 + Harmony(dominant_ | supertonic, leading_tone_ | dominant, supertonic | leading_tone)
h_acc_I_ter = octave_4 + Harmony((tonic - 12) | mediant, tonic | dominant, mediant | (tonic + 12))

phrase_1_acc = (
    (t_acc @ h_acc_I @ (s_accompaniment * len(t_acc))) *
    (t_acc @ h_acc_V @ (s_accompaniment * len(t_acc))) *
    (t_acc @ h_acc_VI @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_I46 @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_V_bis @ (s_accompaniment * len(t_acc_head)))
)

phrase_1 = phrase_1_mel + phrase_1_acc

## Phrase 2
### Melody
h_ph_2_tail = Harmony(
    Chord(supertonic) | Chord(subdominant),
    Chord(tonic) | Chord(mediant),
)
h_ph_2 = h_ph_1_head + h_ph_2_tail
h_ph_2 = octave_melodie + h_ph_2

phrase_2_medi = t_ph_1 @ h_ph_2 @ (s_melody_medi * len(t_ph_1))
phrase_2_treb = t_ph_1 @ (h_ph_2 + 12) @ (s_melody_medi * len(t_ph_1))
phrase_2_mel = phrase_2_medi  # parallelization(phrase_2_medi, phrase_2_treb)

### Accompaniment
phrase_2_acc = (
    (t_acc @ h_acc_I @ (s_accompaniment * len(t_acc))) *
    (t_acc @ h_acc_V @ (s_accompaniment * len(t_acc))) *
    (t_acc @ h_acc_VI @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_V_bis @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_I @ (s_accompaniment * len(t_acc_head)))
)

phrase_2 = phrase_2_mel + phrase_2_acc

## Phrase 3
### Melody
t_ph_3 = t_1 * t_4 * t_4 * t_2_bis

h_ph_3_1 = Harmony(supertonic | subdominant, mediant | dominant, tonic | mediant)
h_ph_3_2 = Harmony(supertonic | subdominant, mediant | dominant, subdominant | submediant, tonic | mediant)
h_ph_3_3 = Harmony(supertonic | subdominant, mediant | dominant, subdominant | submediant, supertonic | subdominant)
h_ph_3_4 = Harmony(tonic | mediant, supertonic | subdominant, dominant_ | leading_tone_, mediant | dominant)

h_ph_3 = h_ph_3_1 + h_ph_3_2 + h_ph_3_3 + h_ph_3_4
h_ph_3 = octave_melodie + h_ph_3

phrase_3_medi = t_ph_3 @ h_ph_3 @ (s_melody_medi * len(t_ph_3))
phrase_3_treb = t_ph_3 @ (h_ph_3 + 12) @ (s_melody_medi * len(t_ph_3))
phrase_3_mel = phrase_3_medi  # parallelization(phrase_3_medi, phrase_3_treb)
phrase_3_mel.end -= frac(1, 4)

### Accompaniment
h_acc_I = octave_4 + Harmony(tonic | dominant, mediant | (tonic + 12), dominant | (mediant + 12))
h_acc_V = octave_4 + Harmony(dominant_ | subdominant, supertonic | leading_tone, subdominant | (supertonic + 12))
h_acc_VI = octave_4 + Harmony(submediant_ | mediant, tonic | dominant, mediant | (tonic + 12))
h_acc_V_V = octave_4 + Harmony(supertonic_ | supertonic, superdominant_ | subdominant, tonic | superdominant)

phrase_3_acc = (
    (t_acc_head @ h_acc_V @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_I @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_V @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_I @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_V @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_VI @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_V_V @ (s_accompaniment * len(t_acc_head))) *
    (t_acc_head @ h_acc_V @ (s_accompaniment * len(t_acc_head)))
)

phrase_3 = phrase_3_mel + phrase_3_acc

## Phrase 4
### Melody
t_ph_4 = t_1_bis * t_2 * t_1 * t_3
h_ph_4 = Harmony(
    mediant | dominant,
    subdominant | submediant,
    dominant | subtonic,
    dominant | subtonic,
    subdominant | submediant,
    mediant | dominant,
    supertonic | subdominant,
    tonic | mediant,
    supertonic | subdominant,
    mediant | dominant,
    supertonic | subdominant,
    tonic | mediant,
)

h_ph_4 = octave_melodie + h_ph_4

phrase_4_medi = t_ph_4 @ h_ph_4 @ (s_melody_medi * len(t_ph_4))
phrase_4_treb = t_ph_4 @ (h_ph_4 + 12) @ (s_melody_medi * len(t_ph_4))
phrase_4_mel = phrase_4_medi  # parallelization(phrase_4_medi, phrase_4_treb)

phrase_4_acc = phrase_2_acc

phrase_4 = phrase_4_mel + phrase_4_acc

## Full piece
melody = phrase_1_mel * phrase_2_mel * phrase_3_mel * phrase_4_mel
accompaniment = phrase_1_acc * phrase_2_acc * phrase_3_acc * phrase_4_acc

piece = phrase_1 * phrase_2 * phrase_3 * phrase_4
# piece = parallelization(melody, accompaniment)

# Paths
name = 'ode_melancolie'
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

# Write MIDI
midi = piece.to_midi(bpm=60*2, velocity=80)
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
