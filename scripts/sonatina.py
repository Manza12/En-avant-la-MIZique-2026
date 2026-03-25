from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument
from musictensors.plot import plot_notes, plt

Chord.default_velocity = 90

# Tonic
G4 = Pitch(67)

# Octaves
octave_4 = G4
octave_3 = G4 - 12
octave_2 = G4 - 12 * 2
octave_5 = G4 + 12
octave_6 = G4 + 12 * 2

# Orquestration
piano = Instrument('Acoustic Grand Piano')

# Textures
## Atomic textures
t_dotted_half = Texture(Rhythm(Hit('0', '3/4')))
t_half = Texture(Rhythm(Hit('0', '1/2')))
t_quarter = Texture(Rhythm(Hit('0', '1/4')))
t_dotted_quarter = Texture(Rhythm(Hit('0', '3/8')))
t_4_12 = Texture(Rhythm(Hit('0', '4/12')))
t_5_16 = Texture(Rhythm(Hit('0', '5/16')))
t_dotted_eighth = Texture(Rhythm(Hit('0', '3/16')))
t_eighth = Texture(Rhythm(Hit('0', '1/8')))
t_triplet_eighth = Texture(Rhythm(Hit('0', '1/12')))
t_sixteenth = Texture(Rhythm(Hit('0', '1/16')))

## Molecular textures
t_3_quarters = t_quarter ** 3
t_half_quarter = t_half * t_quarter
t_6_eighths = t_eighth ** 6
t_2_quarter_p = t_quarter + t_quarter

## Melodic textures
### Theme A
t_theme_A_head = t_dotted_quarter * t_eighth ** 3

### Theme B
t_theme_B_head = t_4_12 * t_triplet_eighth ** 5
t_theme_B_head_bis = t_5_16 * t_sixteenth ** 7
t_theme_B2_1 = t_quarter * t_sixteenth ** 4 * t_dotted_eighth * t_sixteenth
t_theme_B2_2 = t_quarter * t_eighth * t_sixteenth ** 6
t_theme_B2_3 = t_eighth ** 2

((t_theme_B_head * t_half_quarter @ h_theme_B_1) *
            (t_theme_B_head_bis * t_half_quarter @ h_theme_B_2) *
            (t_theme_B_head_bis * t_6_eighths @ h_theme_B_3) *
            (t_theme_B2_1 @ h_theme_B2_1) *
            (t_theme_B2_2 @ h_theme_B2_2) *
            (t_theme_B2_3 @ h_theme_B2_3) *
            (t_theme_B2_4 @ h_theme_B2_4) *
            (t_theme_B2_4 @ h_theme_B2_5) *
            (t_coup @ h_I_coup_mel))


## Accompaniment textures
t_alberti_1 = Texture(
    Rhythm(Hit('0/8', '1/8')),
    Rhythm(Hit('2/8', '1/8'), Hit('4/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8'), Hit('5/8', '1/8')),
)

t_alberti_2_a = Texture(
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('0/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
)

t_alberti_2_b = Texture(
    Rhythm(Hit('0/8', '1/8')),
    Rhythm(Hit('1/8', '1/8')),
)

t_alberti_cad = Texture(
    Rhythm(Hit('0/8', '1/8'), Hit('4/8', '2/8')),
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
)







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

supertonic_sharp = Chord({3})

supertonic_ = supertonic + (-12)
mediant_ = mediant + (-12)
subdominant_ = subdominant + (-12)
tritone_ = tritone + (-12)
dominant_ = dominant + (-12)
submediant_ = submediant + (-12)
leading_tone_ = leading_tone + (-12)

h_I = octave_3 + Harmony(tonic, mediant, dominant)
h_Ino3 = octave_3 + Harmony(tonic, dominant)
h_V34 = octave_3 + Harmony(supertonic, subdominant, dominant)
h_V6 = octave_3 + Harmony(leading_tone_, supertonic, dominant)
h_V_prime = octave_3 + Harmony(dominant_, tritone, dominant)

## Theme A
h_theme_A_1 = octave_4 + Harmony(tonic, mediant, tonic, mediant, dominant, dominant, dominant)
h_theme_A_2 = octave_4 + Harmony(dominant, mediant + 12, supertonic + 12, tonic + 12, tonic + 12, leading_tone)
h_theme_A_3 = octave_4 + Harmony(supertonic + 12, leading_tone, dominant, subdominant, supertonic_sharp, mediant, submediant, dominant, mediant, tonic)
h_theme_A_4 = octave_4 + Harmony(leading_tone_, leading_tone_ | subdominant, tonic | mediant, tonic | mediant, leading_tone_ | supertonic)

# Structure
## Theme A
### Melody
melody_1 = ((t_theme_A_head * t_3_quarters @ h_theme_A_1) *
            (t_theme_A_head * t_half_quarter @ h_theme_A_2) *
            (t_theme_A_head * t_6_eighths @ h_theme_A_3) *
            (t_3_quarters * t_half_quarter @ h_theme_A_4))

### Accompaniment
accompaniment_1 = ((t_alberti_1 ** 2 @ (h_I * 2)) *
                   (t_alberti_1 ** 2 @ (h_I + h_V34)) *
                   (t_alberti_1 ** 2 @ (h_V6 + h_I)) *
                   (t_alberti_2_a * t_alberti_2_b * t_alberti_cad @ (h_V34 + h_Ino3 + h_V_prime)))

phrase_1 = accompaniment_1  + melody_1

## Theme A
### Melody
melody_2 = ((t_theme_B_head * t_half_quarter @ h_theme_B_1) *
            (t_theme_B_head_bis * t_half_quarter @ h_theme_B_2) *
            (t_theme_B_head_bis * t_6_eighths @ h_theme_B_3) *
            (t_theme_B2_1 @ h_theme_B2_1) *
            (t_theme_B2_2 @ h_theme_B2_2) *
            (t_theme_B2_3 @ h_theme_B2_3) *
            (t_theme_B2_4 @ h_theme_B2_4) *
            (t_theme_B2_4 @ h_theme_B2_5) *
            (t_coup @ h_I_coup_mel))

### Accompaniment
accompaniment_2 = ((t_acc_B_head @ h_Ino5) *
                   (t_acc_B_tail @ h_viino5) *
                   (t_acc_B_head @ h_vii) *
                   (t_acc_B_tail @ h_Ino5) *
                   (t_acc_B_head @ h_Ino1) *
                   (t_acc_B_tail_prime @ h_IVno5) *
                   (t_cad_1 @ h_dom8) *
                   (t_coup @ h_I_coup_acc) *
                   (t_theme_B2_4 @ h_theme_B2_acc) *
                   (t_eighth_full @ h_ton) *
                   (t_dotted_half @ h_V7no35) *
                   (t_coup @ h_I_coup_acc))

phrase_2 = accompaniment_2  + melody_2

## Full piece
piece = phrase_1 @ piano

# Paths
name = Path(__file__).stem
midi_path = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

# Write MIDI
midi = piece.to_midi(bpm=120)
midi.write(midi_path)

# Render MIDI to audio
render_midi_to_audio(
    midi_path,
    audio_path,
    sf2_path
)

# Plot
plot_notes(piece, figsize=(8, 3), x_tick_start=0, x_tick_step=1)
plt.tight_layout()

# Save the plot as a vector image (SVG)
plt.savefig(f'../plots/{name}.svg', format='svg')

plt.show()
