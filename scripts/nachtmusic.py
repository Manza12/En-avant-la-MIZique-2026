from pathlib import Path

from musictensors.audio import render_midi_to_audio
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
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('3/8', '1/8')),
)

t_2 = Texture(
    Rhythm(Hit('0', '1/8')),
    Rhythm(Hit('1/8', '1/8')),
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('3/8', '1/8')),
    Rhythm(Hit('4/8', '1/4')),
)
t_2.end += frac(1, 4)

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

t_3_a = t_3_head_a * t_3_tail
t_3_b = t_3_head_b * t_3_tail
t_3_c = t_3_head_c * t_3_tail

t_4_a = Texture(
    Rhythm(Hit('0', '1/16'), Hit('1/16', '1/16'), Hit('2/16', '1/16'), Hit('3/16', '1/16'),
           Hit('4/16', '1/16'), Hit('5/16', '1/16'), Hit('6/16', '1/16'), Hit('7/16', '1/16'))
)
t_4_b = Texture(
    Rhythm(Hit('0', '1/8'), Hit('1/8', '1/8'), Hit('2/8', '1/8'), Hit('3/8', '1/8'))
)
t_4_c = Texture(
    Rhythm(Hit('0', '1/8'))
) ** 4

# Harmony
tonic = Chord({0})
supertonic = Chord({2})
mediant = Chord({3})
subdominant = Chord({5})
tritone = Chord({6})
dominant = Chord({7})
submediant = Chord({8})
leading_tone = Chord({11})

supertonic_ = supertonic - 12
mediant_ = mediant - 12
subdominant_ = subdominant - 12
tritone = tritone - 12
dominant_ = dominant - 12
submediant_ = submediant - 12
leading_tone_ = leading_tone - 12

# Orquestration
violin = Instrument('Violin')
viola = Instrument('Viola')
bass = Section(Instrument('Cello'), Instrument('Contrabass'))

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
piece = ph_1 * ph_2

# Paths
name = 'nachtmusic'
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
