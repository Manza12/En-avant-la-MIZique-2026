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

t_a = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('3/8', '1/8')),
)
t_b = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('1/4', '1/4')),
)

# Orquestration
piano = Instrument('Acoustic Grand Piano')
s_piano = Section(piano)
s_flute_pan = Section(Instrument('Pan FLute'))
s_timpani = Section(Instrument('Timpani'), Instrument('Cello'), Instrument('Contrabass'))
s_brass = Section(Instrument('Trombone'), Instrument('French Horn'), Instrument('Trumpet'))

s_accompaniment_a = s_timpani
s_accompaniment_b = s_brass
s_melody = s_flute_pan

# Harmony
## Tonal degrees
tonic = Chord({0})
supertonic = Chord({2})
mediant = Chord({3})
subdominant = Chord({5})
tritone = Chord({6})
dominant = Chord({7})
dominant_plus = Chord({8})
submediant = Chord({8})
leading_tone = Chord({10})

supertonic_ = supertonic + (-12)
mediant_ = mediant + (-12)
subdominant_ = subdominant + (-12)
tritone = tritone + (-12)
dominant_ = dominant + (-12)
submediant_ = submediant + (-12)
leading_tone_ = leading_tone + (-12)

# Phrases
## Phrase 1
### Melody
t_ph_1 = t_1 * t_2 * t_1 * t_3
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
h_ph_1 = octave_4 + (h_ph_1 | (h_ph_1 + 12))

phrase_1_mel = t_ph_1 @ h_ph_1 @ (s_melody * len(t_ph_1))

### Accompaniment
t_ph_1_acc_a = t_a * t_a * t_a * t_a
t_ph_1_acc_b = t_2 * t_3

h_ph_1_acc_head_a = octave_3 + Harmony(
    (tonic + -12 | dominant_ | tonic | mediant),
    (tonic + -24 | tonic + -12),
    (tonic + -12 | tonic),
    (tonic + -24 | tonic + -12),
    (dominant_ | dominant),
    (dominant_ + -12 | dominant + -12),
    (dominant_ | dominant),
    (dominant_ + -12 | dominant + -12),
)
h_ph_1_acc_head_b = octave_3 + Harmony(
    (tonic + -24 | tonic + -12),
    (tonic + -12 | mediant_ | dominant_ | tonic),
    (leading_tone_ + -12 | dominant_ | supertonic),
    (tonic + -12 | dominant_ | mediant),
)
h_ph_1_acc_tail = octave_3 + Harmony(
    (dominant_ | tonic | mediant),
    (dominant_ | leading_tone_ | supertonic),
)

phrase_1_acc_a = t_ph_1_acc_a @ h_ph_1_acc_head_a @ (s_accompaniment_a * len(t_ph_1_acc_a))
phrase_1_acc_b = t_ph_1_acc_b @ (h_ph_1_acc_head_b + h_ph_1_acc_tail) @ (s_accompaniment_b * len(t_ph_1_acc_b))

phrase_1_acc = phrase_1_acc_a * phrase_1_acc_b

phrase_1 = phrase_1_mel + phrase_1_acc

## Phrase 2
### Melody
h_ph_2_tail = Harmony(
    Chord(supertonic),
    Chord(tonic),
)
h_ph_2 = h_ph_1_head + h_ph_2_tail
h_ph_2 = octave_4 + (h_ph_2 | (h_ph_2 + 12))
phrase_2_mel = t_ph_1 @ h_ph_2 @ (s_melody * len(t_ph_1))

### Accompaniment
h_ph_2_acc_tail = octave_3 + Harmony(
    (dominant_ | leading_tone_ | supertonic | dominant),
    ((tonic - 12) | mediant_ | dominant_ | tonic),
)

phrase_2_acc_a = t_ph_1_acc_a @ h_ph_1_acc_head_a @ (s_accompaniment_a * len(t_ph_1_acc_a))
phrase_2_acc_b = t_ph_1_acc_b @ (h_ph_1_acc_head_b + h_ph_2_acc_tail) @ (s_accompaniment_b * len(t_ph_1_acc_b))

phrase_2_acc = phrase_2_acc_a * phrase_2_acc_b

phrase_2 = phrase_2_mel + phrase_2_acc

## Phrase 3
### Melody
t_ph_3 = t_1 * t_4 * t_4 * t_2_bis

h_ph_3_1 = Harmony(supertonic, mediant, tonic)
h_ph_3_2 = Harmony(supertonic, mediant, subdominant, tonic)
h_ph_3_3 = Harmony(supertonic, mediant, subdominant, supertonic)
h_ph_3_4 = Harmony(tonic, supertonic, dominant_, mediant)

h_ph_3 = h_ph_3_1 + h_ph_3_2 + h_ph_3_3 + h_ph_3_4
h_ph_3 = octave_4 + (h_ph_3 | (h_ph_3 + 12))

phrase_3_mel = t_ph_3 @ h_ph_3 @ (s_melody * len(t_ph_3))

### Accompaniment
h_ph_3_acc_1 = octave_3 + Harmony(
    (dominant_ | leading_tone_ | supertonic),
    (dominant_ + -24 | dominant_ + -12),
)
h_ph_3_acc_2 = octave_3 + Harmony(
    (dominant + -24 | dominant + -12),
    (tonic - 12 | mediant_ | dominant_ | tonic),
)
h_ph_3_acc_3 = octave_3 + Harmony(
    (dominant_ | leading_tone_ | supertonic | dominant),
    (dominant_ + -12 | dominant_),
)
h_ph_3_acc_4 = octave_3 + Harmony(
    (dominant + -24 | dominant + -12),
    (tonic - 12 | mediant_ | dominant_ | tonic),
)
h_ph_3_acc_5 = octave_3 + Harmony(
    (dominant_ | leading_tone_ | supertonic | dominant),
    (dominant_ + -12 | dominant_),
)
h_ph_3_acc_6 = octave_3 + Harmony(
    (dominant_plus + -12 | dominant_plus),
    (mediant_ + -12 | mediant_),
)
h_ph_3_acc_end = octave_3 + Harmony(
    (submediant_ + -12 | submediant_),
    (supertonic_ + -12 | supertonic_),
    (dominant_ + -12 | dominant_),
    (dominant_ | tonic | mediant)
)

phrase_3_acc = (
    (t_a @ h_ph_3_acc_1 @ (s_accompaniment_a * len(t_a))) *
    (t_b @ h_ph_3_acc_2 @ (s_accompaniment_b * len(t_b))) *
    (t_a @ h_ph_3_acc_3 @ (s_accompaniment_a * len(t_a))) *
    (t_b @ h_ph_3_acc_4 @ (s_accompaniment_b * len(t_b))) *
    (t_a @ h_ph_3_acc_5 @ (s_accompaniment_a * len(t_a))) *
    (t_b @ h_ph_3_acc_6 @ (s_accompaniment_b * len(t_b))) *
    (t_2 @ h_ph_3_acc_end @ (s_accompaniment_b * len(t_2)))
)

phrase_3 = phrase_3_mel + phrase_3_acc
phrase_3.end -= frac(1, 4)

## Phrase 4
t_ph_4 = t_1_bis * t_2 * t_1 * t_3

h_ph_3_1 = Harmony(supertonic, mediant, tonic)
h_ph_3_2 = Harmony(supertonic, mediant, subdominant, tonic)
h_ph_3_3 = Harmony(supertonic, mediant, subdominant, supertonic)
h_ph_3_4 = Harmony(tonic, supertonic, dominant_, mediant)

h_ph_4 = Harmony(
    mediant,
    subdominant,
    dominant,
    dominant,
    subdominant,
    mediant,
    supertonic,
    tonic,
    supertonic,
    mediant,
    supertonic,
    tonic,
)
h_ph_4 = octave_4 + (h_ph_4 | (h_ph_4 + 12))

phrase_4_mel = t_ph_4 @ h_ph_4 @ (s_melody * len(t_ph_4))
phrase_4 = phrase_4_mel + phrase_2_acc


## Full piece
piece = phrase_1 * phrase_2 * phrase_3 * phrase_4

# Paths
name = 'ode_joie_medieval'
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

# Write MIDI
midi = piece.to_midi(bpm=80*2, velocity=80)
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
