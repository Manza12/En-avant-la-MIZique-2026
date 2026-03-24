from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument, Section
from musictensors.plot import plot_notes, plt
from musictensors import frac

# Tonic
G4 = Pitch(67)

# Octaves
octave_4 = G4
octave_3 = G4 - 12
octave_2 = G4 - 12 * 2
octave_5 = G4 + 12
octave_6 = G4 + 12 * 2

# Textures
t_1 = Texture(
    Rhythm(Hit('0', '1/2')),
    Rhythm(Hit('0', '1/2')),
)

t_2 = Texture(
    Rhythm(Hit('0', '1')),
    Rhythm(Hit('0', '1')),
    Rhythm(Hit('0', '1')),
    Rhythm(Hit('0', '1')),
    Rhythm(Hit('0', '1')),
)

t_3_head_a = Texture(Rhythm(Hit('0', '1/8')))
t_3_head_a.end = frac(1, 4)

t_3_head_b = Texture(
    Rhythm(Hit('0', '1/24'), Hit('2/24', '1/24')),
    Rhythm(Hit('1/24', '1/24')),
    Rhythm(Hit('1/8', '1/8')),
)

t_3_head_c = Texture(
    Rhythm(Hit('0', '1/8')),
    Rhythm(Hit('1/8', '1/8')),
)

t_3_tail = Texture(
    Rhythm(Hit('0', '3/8')),
    Rhythm(Hit('3/8', '1/8')),
    Rhythm(Hit('4/8', '1/8')),
    Rhythm(Hit('5/8', '1/8')),
)

t_3_a = Texture(Rhythm(Hit('0', '1'))) * 5
t_3_b = Texture(Rhythm(Hit('0', '1'))) * 7
t_3_c = Texture(Rhythm(Hit('0', '1'))) * 6

t_4_a = Texture(
    Rhythm(Hit('0', '1/2'))
)
t_4_b = Texture(
    Rhythm(Hit('0', '1/2'))
)
t_4_c = Texture(
    Rhythm(Hit('0', '1/2'))
) * 4

# Harmony
tonic = Chord({0})
supertonic = Chord({2})
mediant = Chord({4})
subdominant = Chord({5})
tritone = Chord({6})
dominant = Chord({7})
submediant = Chord({9})
leading_tone = Chord({11})

supertonic_ = supertonic - 12
mediant_ = mediant - 12
subdominant_ = subdominant - 12
tritone = tritone - 12
dominant_ = dominant - 12
submediant_ = submediant - 12
leading_tone_ = leading_tone - 12

# Orquestration
violin = Instrument('Acoustic Grand Piano')
viola = Instrument('Acoustic Grand Piano')
bass = Section(Instrument('Acoustic Grand Piano'))
piano = Instrument('Acoustic Grand Piano')

# Phrase 1
## Antecedent
### Measure 1
h = Harmony((dominant_ - 12) | mediant_ | tonic, dominant_)
h_ = Harmony(tonic, dominant_)

m_1_vln = ((t_1 @ (octave_5 + h)) * (t_1 @ (octave_5 + h_))) @ violin
m_1_vla = (t_1 @ (octave_4 + h_)) ** 2 @ viola
m_1_bass = (t_1 @ (octave_3 + h_)) ** 2 @ bass

m_1 = m_1_vln + m_1_vla + m_1_bass

### Measure 2
h = Harmony(tonic, dominant_, tonic, mediant, dominant)

m_2_vln = t_2 @ (octave_5 + h) @ violin
m_2_vla = t_2 @ (octave_4 + h) @ viola
m_2_bass = t_2 @ (octave_3 + h) @ bass

m_2 = m_2_vln + m_2_vla + m_2_bass

## Consecuent
### Measure 3
h = Harmony(subdominant, supertonic)

m_3_vln = (t_1 @ (octave_5 + h)) ** 2 @ viola
m_3_vla = (t_1 @ (octave_4 + h)) ** 2 @ viola
m_3_bass = (t_1 @ (octave_3 + h)) ** 2 @ bass

m_3 = m_3_vln + m_3_vla + m_3_bass

### Measure 4
h = Harmony(subdominant, supertonic, leading_tone_, supertonic, dominant_)

m_4_vln = t_2 @ (octave_5 + h) @ violin
m_4_vla = t_2 @ (octave_4 + h) @ viola
m_4_bass = t_2 @ (octave_3 + h) @ bass

m_4 = m_4_vln + m_4_vla + m_4_bass

ph_1 = m_1 * m_2 * m_3 * m_4

# Phrase 2
## Melody
h_5_mel = octave_5 + Harmony(dominant_ - 12 | mediant_ | tonic, tonic, mediant, supertonic, tonic)
h_6_mel = octave_5 + Harmony(tonic, supertonic, leading_tone_, leading_tone_, supertonic, subdominant, leading_tone_)
h_7_mel = octave_5 + Harmony(supertonic, tonic, tonic, mediant, supertonic, tonic)

m_5_mel = t_3_a @ h_5_mel
m_6_mel = t_3_b @ h_6_mel
m_7_mel = t_3_c @ h_7_mel
m_8_mel = m_6_mel

ph_2_mel = (m_5_mel * m_6_mel * m_7_mel * m_8_mel) @ violin

## Accompaniment
ph_2_acc_vln = ((t_4_a @ (octave_3 + Harmony(mediant | dominant))) ** 2
                * (t_4_a @ (octave_3 + Harmony(subdominant | dominant))) ** 2) ** 2 @ violin
ph_2_acc_vla = ((t_4_b @ (octave_4 + Harmony(tonic))) ** 2
                * (t_4_b @ (octave_4 + Harmony(supertonic)))
                * (t_4_c @ (octave_4 + Harmony(supertonic, subdominant, leading_tone_, supertonic)))) ** 2 @ viola
ph_2_acc_bass = (t_4_b @ (octave_3 + Harmony(tonic))) ** 8 @ bass

ph_2_acc = ph_2_acc_vln + ph_2_acc_vla + ph_2_acc_bass

ph_2 = ph_2_mel + ph_2_acc

## End
t_quarter = Texture(Rhythm(Hit('0', '1/4')))
h_1 = octave_3 + Harmony(Chord({0, 7, 4, 7, 24}))
h_2 = octave_3 + Harmony(Chord({2, 7, 17, 24, 23, 21}))
h_3 = octave_3 + Harmony(Chord({4, 7, 19, 24}))
h_4 = octave_3 + Harmony(Chord({-1, 7, 17, 16, 14, 24, 26, 28}))
h_5 = octave_3 + Harmony(Chord({0, 7, 12, 28}))
h_6 = octave_3 + Harmony(Chord({2, 7, 11, 31, 29, 28}))
h_7 = octave_3 + Harmony(Chord({4, 7, 12, 31}))

end = t_quarter ** 7 @ (h_1 + h_2 + h_3 + h_4 + h_5 + h_6 + h_7) @ bass

# Full piece
piece = ph_1 * ph_2 * end

# Only harmony
t_half_2 = Texture(Rhythm(Hit('0', '1/2'))) * 2
t_half_1 = Texture(Rhythm(Hit('0', '1/2'))) * 1
t_half_4 = Texture(Rhythm(Hit('0', '1/2'))) * 4
t_whole_5 = Texture(Rhythm(Hit('0', '1/1'))) * 5
t_whole_6 = Texture(Rhythm(Hit('0', '1/1'))) * 6
t_whole_7 = Texture(Rhythm(Hit('0', '1/1'))) * 7

t_1 = t_half_2
t_2 = t_whole_5
t_3_a = t_whole_5
t_3_b = t_whole_7
t_3_c = t_whole_6
t_4_a = t_half_1
t_4_b = t_half_1
t_4_c = t_half_4

violin = piano
viola = piano
bass = piano

# Phrase 1
## Antecedent
### Measure 1
h = Harmony((dominant_ - 12) | mediant_ | tonic, dominant_)
h_ = Harmony(tonic, dominant_)

m_1_vln = ((t_1 @ (octave_5 + h)) * (t_1 @ (octave_5 + h_))) @ violin
m_1_vla = (t_1 @ (octave_4 + h_)) ** 2 @ viola
m_1_bass = (t_1 @ (octave_3 + h_)) ** 2 @ bass

m_1 = m_1_vln + m_1_vla + m_1_bass

### Measure 2
h = Harmony(tonic, dominant_, tonic, mediant, dominant)

m_2_vln = t_2 @ (octave_5 + h) @ violin
m_2_vla = t_2 @ (octave_4 + h) @ viola
m_2_bass = t_2 @ (octave_3 + h) @ bass

m_2 = m_2_vln + m_2_vla + m_2_bass

## Consecuent
### Measure 3
h = Harmony(subdominant, supertonic)

m_3_vln = (t_1 @ (octave_5 + h)) ** 2 @ viola
m_3_vla = (t_1 @ (octave_4 + h)) ** 2 @ viola
m_3_bass = (t_1 @ (octave_3 + h)) ** 2 @ bass

m_3 = m_3_vln + m_3_vla + m_3_bass

### Measure 4
h = Harmony(subdominant, supertonic, leading_tone_, supertonic, dominant_)

m_4_vln = t_2 @ (octave_5 + h) @ violin
m_4_vla = t_2 @ (octave_4 + h) @ viola
m_4_bass = t_2 @ (octave_3 + h) @ bass

m_4 = m_4_vln + m_4_vla + m_4_bass

ph_1 = m_1 * m_2 * m_3 * m_4

# Phrase 2
## Melody
h_5_mel = octave_5 + Harmony(dominant_ - 12 | mediant_ | tonic, tonic, mediant, supertonic, tonic)
h_6_mel = octave_5 + Harmony(tonic, supertonic, leading_tone_, leading_tone_, supertonic, subdominant, leading_tone_)
h_7_mel = octave_5 + Harmony(supertonic, tonic, tonic, mediant, supertonic, tonic)

m_5_mel = t_3_a @ h_5_mel
m_6_mel = t_3_b @ h_6_mel
m_7_mel = t_3_c @ h_7_mel
m_8_mel = m_6_mel

ph_2_mel = (m_5_mel * m_6_mel * m_7_mel * m_8_mel) @ violin

## Accompaniment
ph_2_acc_vln = ((t_4_a @ (octave_3 + Harmony(mediant | dominant))) ** 2
                * (t_4_a @ (octave_3 + Harmony(subdominant | dominant))) ** 2) ** 2 @ violin
ph_2_acc_vla = ((t_4_b @ (octave_4 + Harmony(tonic))) ** 2
                * (t_4_b @ (octave_4 + Harmony(supertonic)))
                * (t_4_c @ (octave_4 + Harmony(supertonic, subdominant, leading_tone_, supertonic)))) ** 2 @ viola
ph_2_acc_bass = (t_4_b @ (octave_3 + Harmony(tonic))) ** 8 @ bass

ph_2_acc = ph_2_acc_vln + ph_2_acc_vla + ph_2_acc_bass

ph_2 = ph_2_mel + ph_2_acc

# Full piece
piece_harmony = ph_1 * ph_2

# Paths
name = Path(__file__).stem
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

midi_path_harmony = Path(f'../midi/{name}-harmony.mid')
audio_path_harmony = Path(f'../audio/{name}-harmony.wav')

# Write MIDI
midi = piece.to_midi(bpm=80*2)
midi.write(midi_path)

midi_harmony = piece_harmony.to_midi(bpm=80*2)
midi_harmony.write(midi_path_harmony)

# Render MIDI to audio
render_midi_to_audio(
    midi_path,
    audio_path,
    sf2_path
)

render_midi_to_audio(
    midi_path_harmony,
    audio_path_harmony,
    sf2_path
)

# Plot
plot_notes(piece,
           figsize=(12, 6),
           x_tick_start=0,
           x_tick_step=1,)
plt.show()
