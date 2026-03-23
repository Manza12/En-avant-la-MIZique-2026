from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument, Section
from musictensors.plot import plot_notes, plt

Chord.default_velocity = 90

# Tonic
D4 = Pitch(62)

# Octaves
octave_4 = D4
octave_3 = D4 - 12
octave_2 = D4 - 12 * 2
octave_5 = D4 + 12
octave_6 = D4 + 12 * 2

# Textures
t_1_a = Texture(
    Rhythm(Hit('0', '5/12'), Hit('5/12', '1/12')),
    Rhythm(Hit('6/12', '2/12')),
    Rhythm(Hit('8/12', '3/12')),
    Rhythm(Hit('11/12', '3/12')),
    Rhythm(Hit('15/12', '3/12')),
    Rhythm(Hit('18/12', '3/12')),
    Rhythm(Hit('21/12', '3/12')),
)
t_1_b = Texture(
    Rhythm(Hit('2/12', '3/12'), Hit('5/12', '1/12')),
    Rhythm(Hit('6/12', '2/12')),
    Rhythm(Hit('8/12', '3/12')),
    Rhythm(Hit('11/12', '3/12')),
    Rhythm(Hit('17/12', '1/12'), Hit('18/12', '6/12')),
    # Rhythm(Hit('18/12', '6/12')),
)

t_2_a = t_1_a
t_2_b = Texture(
    Rhythm(Hit('2/12', '1/12'), Hit('3/12', '2/12'), Hit('5/12', '1/12')),
    Rhythm(Hit('6/12', '3/12')),
    Rhythm(Hit('9/12', '3/12')),
    Rhythm(Hit('12/12', '2/12')),
    Rhythm(Hit('14/12', '2/12'), Hit('17/12', '7/12')),
    # Rhythm(Hit('18/12', '6/12')),
)

t_3_a = Texture(
    Rhythm(Hit('0', '5/12'), Hit('5/12', '1/12')),
    Rhythm(Hit('6/12', '2/12')),
    Rhythm(Hit('8/12', '3/12')),
    Rhythm(Hit('14/12', '1/12')),
    Rhythm(Hit('15/12', '2/12')),
    Rhythm(Hit('17/12', '1/12')),
    Rhythm(Hit('18/12', '2/12')),
    Rhythm(Hit('20/12', '4/12')),
)
t_3_b = Texture(
    Rhythm(Hit('2/12', '1/12')),
    Rhythm(Hit('3/12', '2/12')),
    Rhythm(Hit('5/12', '1/12')),
    Rhythm(Hit('6/12', '2/12')),
    Rhythm(Hit('8/12', '3/12')),
    Rhythm(Hit('11/12', '3/12')),
    Rhythm(Hit('14/12', '3/12')),
    Rhythm(Hit('17/12', '3/12')),
    Rhythm(Hit('20/12', '4/12')),
)

t_3 = t_3_a * t_3_b


# Orquestration
piano = Instrument('Acoustic Grand Piano')
saxo = Instrument('Alto Sax')
bass = Instrument('Acoustic Bass')
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
t_ph_1 = t_1_a * t_1_b
h_ph_1_head = Harmony(
    mediant,
    subdominant,
    dominant,
    dominant,
    subdominant,
    mediant,
    supertonic,
    tonic,
    supertonic,
    mediant
)
h_ph_1_tail = Harmony(
    Chord(mediant),
    Chord(supertonic),
)
h_ph_1 = h_ph_1_head + h_ph_1_tail
h_ph_1 = octave_4 + h_ph_1

phrase_1_melody = t_ph_1 @ h_ph_1 @ saxo

### Accompaniment
t_1 = Texture(Rhythm(Hit('0', '5/12')), Rhythm(Hit('5/12', '7/12'))) ** 2

h_Dmaj7 = octave_3 + Harmony(tonic | mediant | dominant | leading_tone)
h_Fsm7 = octave_3 + Harmony(mediant | dominant | leading_tone | supertonic + 12)
h_Bm7 = octave_3 + Harmony(submediant_ | tonic | mediant | dominant)
h_Em7 = octave_3 + Harmony(supertonic | subdominant | submediant | tonic + 12)
h_A7 = octave_3 + Harmony(dominant_ | leading_tone_ | supertonic | subdominant)

phrase_1_accompaniment = ((t_1 @ (h_Dmaj7 + h_Bm7 + h_Em7 + h_A7) @ s_piano) *
                          (t_1 @ (h_Fsm7 + h_Bm7 + h_Em7 + h_A7) @ s_piano))

### Bass
t_bass = Texture(Rhythm(Hit('0', '1/2'))) ** 8
h_bass = octave_2 + Harmony(tonic, submediant_, supertonic, dominant_, mediant, submediant_, supertonic, dominant_,)
phrase_1_bass = t_bass @ h_bass @ bass

### Full phrase 1
phrase_1 = phrase_1_melody + phrase_1_accompaniment + phrase_1_bass


## Phrase 2
t_ph_2 = t_2_a * t_2_b
h_ph_2_tail = Harmony(
    Chord(supertonic),
    Chord(tonic),
)
h_ph_2 = h_ph_1_head + h_ph_2_tail
h_ph_2 = octave_4 + h_ph_2

### Accompaniment
h_A7 = octave_3 + Harmony(dominant_ | leading_tone_ | supertonic | subdominant)

phrase_2_melody = t_ph_2 @ h_ph_2 @ saxo
phrase_2_accompaniment = ((t_1 @ (h_Dmaj7 + h_Bm7 + h_Em7 + h_A7) @ s_piano) *
                          (t_1 @ (h_Dmaj7 + h_Bm7 + h_A7 + h_Dmaj7) @ s_piano))
h_bass_2 = octave_2 + Harmony(tonic, submediant_, supertonic, dominant_, mediant, submediant_, dominant_, tonic)
phrase_2_bass = t_bass @ h_bass_2 @ bass

phrase_2 = phrase_2_melody + phrase_2_accompaniment + phrase_2_bass

## Phrase 3
t_ph_3 = t_3_a * t_3_b
h_ph_3_1 = Harmony(Chord(supertonic), Chord(mediant), Chord(tonic))
h_ph_3_2 = Harmony(Chord(supertonic), Chord(mediant), Chord(subdominant), Chord(mediant), Chord(tonic))
h_ph_3_3 = Harmony(Chord(supertonic), Chord(mediant), Chord(subdominant), Chord(mediant), Chord(supertonic))
h_ph_3_4 = Harmony(Chord(tonic), Chord(supertonic), Chord(dominant_), Chord(mediant))

h_ph_3 = h_ph_3_1 + h_ph_3_2 + h_ph_3_3 + h_ph_3_4
h_ph_3 = octave_4 + h_ph_3

phrase_3_melody = t_ph_3 @ h_ph_3 @ saxo

# ### Accompaniment
# t_1 = Texture(Rhythm(Hit('0', '5/12')), Rhythm(Hit('5/12', '7/12'))) ** 2
#
# h_Dmaj7 = octave_3 + Harmony(tonic | mediant | dominant | leading_tone)
# h_Fsm7 = octave_3 + Harmony(mediant | dominant | leading_tone | supertonic + 12)
# h_Bm7 = octave_3 + Harmony(submediant_ | tonic | mediant | dominant)
# h_Em7 = octave_3 + Harmony(supertonic | subdominant | submediant | tonic + 12)
# h_A7 = octave_3 + Harmony(dominant_ | leading_tone_ | supertonic | subdominant)
#
# phrase_1_accompaniment = ((t_1 @ (h_Dmaj7 + h_Bm7 + h_Em7 + h_A7) @ s_piano) *
#                           (t_1 @ (h_Fsm7 + h_Bm7 + h_Em7 + h_A7) @ s_piano))
#
# ### Bass
# t_bass = Texture(Rhythm(Hit('0', '1/2'))) ** 8
# h_bass = octave_2 + Harmony(tonic, submediant_, supertonic, dominant_, mediant, submediant_, supertonic, dominant_,
#                             velocity=127)
# phrase_1_bass = t_bass @ h_bass @ bass

### Full phrase 3
phrase_3 = phrase_3_melody # + phrase_3_accompaniment + phrase_3_bass


## Full piece
piece = phrase_1 * phrase_2 * phrase_3 * phrase_2

# Paths
name = Path(__file__).stem
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

# Write MIDI
midi = piece.to_midi(bpm=80*2)
midi.write(midi_path)

# Render MIDI to audio
render_midi_to_audio(
    midi_path,
    audio_path,
    sf2_path
)

# Plot
plot_notes(piece, figsize=(8, 3), x_tick_start=0, x_tick_step=1, color_by_instrument=True)
plt.tight_layout()

# Save the plot as a vector image (SVG)
plt.savefig(f'../plots/{name}.svg', format='svg')

plt.show()
