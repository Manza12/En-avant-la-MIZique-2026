from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument
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
t_vals = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('1/4', '1/4'), Hit('2/4', '1/4')),
)
t_quarter_2 = Texture(Rhythm(Hit('0', '1/4')), Rhythm(Hit('0', '1/4')))
t_unit = Texture(Rhythm(Hit('0', '3/4')), Rhythm(Hit('0', '3/4')))

t_eighth = Texture(Rhythm(Hit('0', '1/8')))
t_quarter = Texture(Rhythm(Hit('0', '1/4')))
t_triple_quarter = Texture(Rhythm(Hit('0', '1/4'), Hit('1/4', '1/4'), Hit('2/4', '1/4')))
t_dotted_quarter = Texture(Rhythm(Hit('0', '3/8')))
t_half = Texture(Rhythm(Hit('0', '1/2')))
t_dotted_half = Texture(Rhythm(Hit('0', '3/4')))

# Orquestration
piano = Instrument('Acoustic Grand Piano')

# Harmony
silence = Chord()

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


h_I = octave_3 + Harmony(tonic, mediant | dominant | (tonic + 12))
h_I46 = octave_3 + Harmony(dominant_, mediant | dominant | (tonic + 12))
h_IV = octave_3 + Harmony(subdominant_, subdominant | submediant | (tonic + 12))
h_V_III = octave_3 + Harmony(subtonic_, subdominant | submediant | (tonic + 12) | supertonic + 12)
h_III = octave_3 + Harmony(mediant, dominant | subtonic | mediant + 12)
h_III46 = octave_3 + Harmony(subtonic_, dominant | subtonic | mediant + 12)
h_II = octave_3 + Harmony(supertonic_, subdominant | submediant | supertonic + 12)
h_I6 = octave_3 + Harmony(mediant_, mediant | dominant | (tonic + 12))
h_I_ = octave_3 + Harmony(tonic - 12, mediant | dominant | (tonic + 12))
h_II7 = octave_3 + Harmony(supertonic_, subdominant | submediant | (tonic + 12))
h_V7 = octave_3 + Harmony(dominant_, subdominant | dominant | leading_tone | (supertonic + 12))


# Phrases
## Phrase 1
### Melody
### Accompaniment
phrase_1_acc = (t_vals ** 16 @ (h_I + h_I46 + h_I + h_I46 + h_IV + h_V_III + h_III + h_III46 +
                               h_IV + h_II + h_I6 + h_I_ + h_II7 + h_V7 + h_I + h_I) @ piano +
                (t_quarter_2 @ h_I @ piano))


## Phrase 2
### Melody
t_melody_1 = t_eighth ** 2 * t_triple_quarter * t_quarter ** 3
t_melody_2 = (t_dotted_half * t_quarter ** 3) ** 2 * t_quarter * t_half
t_melody_3 = t_dotted_half * t_quarter ** 3 * (t_half * t_quarter) ** 2 * t_dotted_half

h_melody_1 = octave_5 + Harmony(tonic, supertonic, mediant, mediant, supertonic, tonic)
h_melody_2 = octave_5 + Harmony(mediant, silence, supertonic, mediant, subdominant, silence, mediant, supertonic, mediant, tonic)
h_melody_3 = octave_5 + Harmony(submediant, subdominant, dominant, submediant, dominant, subdominant, mediant, supertonic, tonic)

phrase_2_melody = (((t_melody_1 + frac(-1, 4)) @ h_melody_1) *
                   (t_melody_2 @ h_melody_2) *
                   ((t_half * t_melody_1) @ (Harmony(silence) + h_melody_1)) *
                   (t_melody_3 @ h_melody_3)) @ piano
# phrase_2_melody -= frac(1, 4)


### Accompaniment
phrase_2_acc = (t_vals ** 15 @ (h_I + h_I46 + h_I + h_I46 + h_IV + h_V7 + h_I + h_I46 +
                               h_I + h_I + h_IV + h_II + h_V7 + h_V7 + h_I) @ piano *
                (t_quarter_2 @ h_I @ piano))

## Full piece
piece = phrase_2_melody + phrase_2_acc

## Harmony
piece_harmony = t_unit ** 15 @ (h_I + h_I46 + h_I + h_I46 + h_IV + h_V7 + h_I + h_I46 +
                                h_I + h_I + h_IV + h_II + h_V7 + h_V7 + h_I) @ piano

# Paths
name = Path(__file__).stem
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

midi_path_harmony = Path(f'../midi/{name}-harmony.mid')
audio_path_harmony = Path(f'../audio/{name}-harmony.wav')

midi_path_accompaniment = Path(f'../midi/{name}-accompaniment.mid')
audio_path_accompaniment = Path(f'../audio/{name}-accompaniment.wav')

# Write MIDI
midi = piece.to_midi(bpm=64*3)
midi.write(midi_path)

midi_harmony = piece_harmony.to_midi(bpm=64*3)
midi_harmony.write(midi_path_harmony)

midi_accompaniment = phrase_2_acc.to_midi(bpm=64*3)
midi_accompaniment.write(midi_path_accompaniment)

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

render_midi_to_audio(
    midi_path_accompaniment,
    audio_path_accompaniment,
    sf2_path
)

plot_notes(piece, figsize=(8, 3), x_tick_start=0, x_tick_step=1)
plt.tight_layout()

# Save the plot as a vector image (SVG)
plt.savefig(f'../plots/{name}.svg', format='svg')

plt.show()
