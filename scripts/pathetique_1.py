from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument
from musictensors.plot import plot_notes, plt
from musictensors import frac

###############
# Definitions #
###############

# Time
## Note values
t_dotted_half = Texture(Rhythm(Hit('0', '3/4')))
t_half = Texture(Rhythm(Hit('0', '1/2')))
t_quarter = Texture(Rhythm(Hit('0', '1/4')))
t_eighth = Texture(Rhythm(Hit('0', '1/8')))

## Textures
t_pedal = Texture(
    Rhythm(Hit('0/8', '1/8'), Hit('2/8', '1/8'), Hit('4/8', '1/8'), Hit('6/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8'), Hit('5/8', '1/8'), Hit('7/8', '1/8')),
)

t_melody_1_head_1 = t_dotted_half * t_quarter
t_melody_1_head_2 = t_quarter * t_half * t_quarter
t_melody_1_tail = t_quarter ** 4

# Frequency
## Pitches and degrees
C4 = Pitch(60)
octave_4 = C4

tonic = Chord({0})
supertonic = Chord({2})
mediant_minor = Chord({3})
mediant_major = Chord({4})
subdominant = Chord({5})
tritone = Chord({6})
dominant = Chord({7})
submediant_minor = Chord({8})
submediant_major = Chord({9})
subtonic = Chord({10})
leading_tone = Chord({11})

supertonic_1 = supertonic - 12
mediant_minor_1 = mediant_minor - 12
mediant_major_1 = mediant_major - 12
subdominant_1 = subdominant - 12
tritone_1 = tritone - 12
dominant_1 = dominant - 12
submediant_minor_1 = submediant_minor - 12
submediant_major_1 = submediant_major - 12
subtonic_1 = subtonic - 12
leading_tone_1 = leading_tone - 12

## Harmonies
h_ton_1 = Harmony.from_chord(tonic)
h_ton_2 = Harmony.from_chord(tonic | tonic + 12)

h_Min_6M = Harmony(mediant_minor_1 | tonic)
h_Maj_6m = Harmony(mediant_major_1 | tonic)
h_Sub_4A = Harmony(subtonic_1 | mediant_major)
h_Smm_6M = Harmony(submediant_minor_1 | subdominant)
h_Maj_3m = Harmony(mediant_major | dominant)
h_Sub_3m = Harmony(subdominant | submediant_minor)
h_Sup_6M = Harmony(supertonic | leading_tone)

#############
# Structure #
#############

# Exposition
### Theme P
#### Phrase 1
##### Measure 1
m1_bass = t_pedal @ (h_ton_2 - 12 * 2)
m1_melody = t_melody_1_head_1 @ (h_ton_1 + h_Sub_4A)
m1 = m1_bass + m1_melody

##### Measure 2
m2_bass = m1_bass
m2_melody = t_melody_1_tail @ (h_Smm_6M + h_Maj_3m + h_Sub_3m + h_Sup_6M)
m2 = m2_bass + m2_melody

##### Measure 3
m3_bass = m1_bass
m3_melody = t_melody_1_head_2 @ ((h_Min_6M + h_Maj_6m + h_Sub_4A) + 12)
m3 = m3_bass + m3_melody

##### Measure 4
m4_bass = m1_bass
m4_melody = m2_melody + 12
m4 = m4_bass + m4_melody

phrase_1 = m1 * m2 * m3 * m4

theme_p = octave_4 + phrase_1

exposition = theme_p

piece = exposition

# Paths
name = "pathetique_1"
midi_path = Path(f'./midi/{name}.mid')
audio_path = Path(f'./audio/{name}.wav')

# Write MIDI
midi = piece.to_midi(bpm=200)
midi.write(midi_path)

# Render MIDI to audio
render_midi_to_audio(
    midi_path,
    audio_path,
    sf2_path
)

# Plot
plot_notes(piece, figsize=(12, 6), x_tick_start=0, x_tick_step=frac(1, 2))
plt.tight_layout()
plt.savefig(f'./plots/{name}.svg', format='svg')
plt.show()
