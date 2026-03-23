from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument
from musictensors.plot import plot_notes, plt
from musictensors import frac

# Tonic
C4 = Pitch(60)

# Octaves
octave_4 = C4
octave_3 = C4 - 12
octave_2 = C4 - 12 * 2
octave_5 = C4 + 12
octave_6 = C4 + 12 * 2

# Textures
t_alberti = Texture(
    Rhythm(Hit('0', '1/8')),
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
)

t_melody_head = Texture(
    Rhythm(Hit('0', '1/2')),
    Rhythm(Hit('1/2', '1/4')),
    Rhythm(Hit('3/4', '1/4')),
)

t_melody_tail_1 = Texture(
    Rhythm(Hit('0', '3/8')),
    Rhythm(Hit('3/8', '1/16'), Hit('1/2', '1/4')),
    Rhythm(Hit('7/16', '1/16')),
)
t_melody_tail_1.end = frac(1, 1)

t_melody_tail_2 = Texture(
    Rhythm(Hit('0', '1/4'), Hit('7/24', '1/24')),
    Rhythm(Hit('1/4', '1/24'), Hit('8/24', '1/24'), Hit('7/16', '1/16')),
    Rhythm(Hit('3/8', '1/16'), Hit('1/2', '1/4')),
)
t_melody_tail_2.end = frac(1, 1)

t_melody_1 = t_melody_head * t_melody_tail_1
t_melody_2 = t_melody_head * t_melody_tail_2

# Harmony
tonic = Chord({0})
supertonic = Chord({2})
mediant = Chord({4})
subdominant = Chord({5})
tritone = Chord({6})
dominant = Chord({7})
submediant = Chord({9})
leading_tone = Chord({11})

supertonic_1 = supertonic - 12
mediant_1 = mediant - 12
subdominant_1 = subdominant - 12
tritone_1 = tritone - 12
dominant_1 = dominant - 12
submediant_1 = submediant - 12
leading_tone_1 = leading_tone - 12

# Orquestration
piano = Instrument('Acoustic Grand Piano')

# Phrase 1
## Antecedent
### Melody
h_1 = octave_5 + Harmony(tonic, mediant, dominant, leading_tone_1, tonic, supertonic)

antecedent_melody = t_melody_1 @ h_1 @ piano

### Accompaniment
h_I = octave_4 + Harmony(tonic, mediant, dominant)
h_V34 = octave_4 + Harmony(supertonic, subdominant, dominant)

antecedent_accompaniment = (t_alberti ** 4) @ (h_I + h_I + h_V34 + h_I) @ piano

antecedent = antecedent_melody + antecedent_accompaniment

## Consequent
### Melody
h_2 = octave_5 + Harmony(submediant, dominant, tonic + 12, dominant, subdominant, mediant)

consequent_melody = t_melody_2 @ h_2 @ piano

### Accompaniment
h_IV64 = octave_4 + Harmony(tonic, subdominant, submediant)
h_V6 = octave_4 + Harmony(leading_tone_1, supertonic, dominant)

consequent_accompaniment = (t_alberti ** 4) @ (h_IV64 + h_I + h_V6 + h_I) @ piano

consequent = consequent_melody + consequent_accompaniment

# Full piece
piece = antecedent * consequent

# Paths
name = 'sonata_16'
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

# Write MIDI
midi = piece.to_midi(bpm=132)
midi.write(midi_path)

# Render MIDI to audio
render_midi_to_audio(
    midi_path,
    audio_path,
    sf2_path
)

# Plot
plot_notes(piece, figsize=(8, 3), x_tick_start=0, x_tick_step=frac(1, 2))  # , color_by_instrument=True
plt.tight_layout()

# Save the plot as a vector image (SVG)
plt.savefig(f'../plots/{name}.svg', format='svg')
plt.show()