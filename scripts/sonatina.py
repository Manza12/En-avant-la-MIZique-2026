from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument
from musictensors.plot import plot_notes, plt
from musictensors import frac

Chord.default_velocity = 90

# Tonic
G4 = Pitch(67)

# Keys
tonic_4 = G4
tonic_3 = G4 - 12
tonic_5 = G4 + 12

dominant_5 = tonic_4 + 7
dominant_4 = tonic_3 + 7
dominant_3 = tonic_3 - 5

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

t_2_quarter_p = Texture(Rhythm(Hit('0', '1/4'), Hit('1/4', '1/4')))
t_3_quarter_p = Texture(Rhythm(Hit('0', '1/4'), Hit('1/4', '1/4'), Hit('2/4', '1/4')))

t_quarter_full = Texture(t_quarter)
t_quarter_full.end = frac(3, 4)

## Melodic textures
### Theme P
t_theme_A_head = t_dotted_quarter * t_eighth ** 3

### Theme S
t_theme_B_head = t_4_12 * t_triplet_eighth ** 5
t_theme_B_head_bis = t_5_16 * t_sixteenth ** 7
t_theme_B2_1 = t_quarter * t_sixteenth ** 4 * t_dotted_eighth * t_sixteenth
t_theme_B2_2 = t_quarter * t_eighth * t_sixteenth ** 6
t_theme_B2_3 = t_eighth ** 2 * t_2_quarter_p
t_theme_B2_4 = t_eighth * t_sixteenth ** 10
t_coup = t_quarter * t_quarter
t_coup.end += frac(1, 4)

t_acc_B_head = Texture(Rhythm(Hit('1/4', '1/4'), Hit('2/4', '1/4')))
t_acc_B_tail = Texture(Rhythm(Hit('0', '1/4'), Hit('1/4', '1/4')))
t_acc_B_tail.end += frac(1, 4)
t_acc_B_tail_prime = Texture(t_quarter)
t_acc_B_tail_prime.end += frac(2, 4)
t_cad_1 = Texture(Rhythm(Hit('0', '1/4'), Hit('2/4', '1/4')), Rhythm(Hit('1/4', '1/4')))
t_eighth_full = Texture(t_eighth)
t_eighth_full.end = frac(3, 4)

### Development
t_dev_3 = Texture(
    Rhythm(Hit('0', '7/32'), Hit('2/8', '1/8'), Hit('4/8', '1/8')),
    Rhythm(Hit('7/32', '1/32')),
    Rhythm(Hit('3/8', '1/8')),
    Rhythm(Hit('5/8', '1/8')),
)
t_dev_4 = t_dotted_quarter * t_sixteenth ** 2 * t_quarter

### Theme P prime
t_theme_P_prime_1 = t_dotted_quarter * t_sixteenth ** 6
t_theme_P_prime_2 = t_eighth * t_quarter * t_eighth ** 3

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

t_alberti_3 = Texture(
    Rhythm(Hit('0/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('4/8', '1/8')),
    Rhythm(Hit('5/8', '1/8')),
)

t_alberti_cad = Texture(
    Rhythm(Hit('0/8', '1/8'), Hit('4/8', '2/8')),
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('1/8', '1/8'), Hit('3/8', '1/8')),
)

# Harmony
## Tonal degrees
silence = Chord()
h_silence = Harmony(silence)

tonic = Chord({0})
supertonic = Chord({2})
mediant = Chord({4})
subdominant = Chord({5})
tritone = Chord({6})
dominant = Chord({7})
submediant = Chord({9})
leading_tone = Chord({11})

led_mediant = Chord({3})
led_submediant = Chord({8})
led_dominant = Chord({6})
led_supertonic = Chord({1})

supertonic_ = supertonic + (-12)
mediant_ = mediant + (-12)
subdominant_ = subdominant + (-12)
tritone_ = tritone + (-12)
dominant_ = dominant + (-12)
submediant_ = submediant + (-12)
leading_tone_ = leading_tone + (-12)

## Chord harmonies
h_I = Harmony(tonic, mediant, dominant)
h_Ino3 = Harmony(tonic, dominant)
h_V34 = Harmony(supertonic, subdominant, dominant)
h_V6 = Harmony(leading_tone_, supertonic, dominant)
h_V_prime = Harmony(dominant_, led_dominant, dominant)
h_iino5 = Harmony(supertonic, subdominant)
h_Ino5 = Harmony(tonic, mediant)
h_viino5 = Harmony(leading_tone_, supertonic)
h_vii = Harmony(leading_tone_, supertonic, subdominant)
h_Ino1 = Harmony(mediant, dominant)
h_IVno5 = Harmony(subdominant, submediant)
h_dom8 = Harmony(dominant_, dominant)
h_ton8 = Harmony(tonic, tonic + 12)
h_ton = Harmony(tonic)
h_V7no35 = Harmony(dominant_, subdominant)
h_V7no3 = Harmony(dominant_, supertonic, subdominant)
h_I46 = Harmony(dominant_, tonic, mediant)
h_V = Harmony(dominant_, leading_tone_, supertonic)
h_IV_46 = Harmony(tonic, subdominant, submediant)
h_V56 = Harmony(leading_tone_, subdominant, dominant)

## Theme P
### Melody
h_theme_A_1 = tonic_4 + Harmony(tonic, mediant, tonic, mediant, dominant, dominant, dominant)
h_theme_A_2 = tonic_4 + Harmony(dominant, mediant + 12, supertonic + 12, tonic + 12, tonic + 12, leading_tone)
h_theme_A_3 = tonic_4 + Harmony(supertonic + 12, leading_tone, dominant, subdominant, led_mediant, mediant, submediant, dominant, mediant, tonic)
h_theme_A_4 = tonic_4 + Harmony(leading_tone_, leading_tone_ | subdominant, tonic | mediant, tonic | mediant, leading_tone_ | supertonic)

## Theme S
### Melody
h_theme_B_1 = dominant_5 + Harmony(dominant_, submediant_, leading_tone_, tonic, supertonic, mediant, dominant, subdominant)
h_theme_B_2 = dominant_5 + Harmony(dominant_, submediant_, leading_tone_, tonic, supertonic, mediant, subdominant, dominant, submediant, dominant)
h_theme_B_3 = dominant_5 + Harmony(tonic, supertonic, mediant, subdominant, dominant, submediant, leading_tone, tonic + 12,
                                   leading_tone, submediant, dominant, subdominant, mediant, supertonic)
h_theme_B2_1 = dominant_5 + Harmony(tonic, supertonic, tonic, leading_tone_, tonic, mediant, supertonic)
h_theme_B2_2 = dominant_5 + Harmony(tonic, silence, mediant, supertonic, tonic, leading_tone_, submediant_, dominant_)
h_theme_B2_3 = dominant_5 + Harmony(subdominant_, silence, supertonic_ | subdominant_)
h_theme_B2_4 = dominant_5 + Harmony(mediant_, dominant, subdominant, mediant, supertonic, tonic, leading_tone_, submediant_, dominant_, subdominant_, mediant_)
h_theme_B2_5 = dominant_5 + Harmony(supertonic_, subdominant, mediant, supertonic, tonic, leading_tone_, submediant_, dominant_, subdominant_, mediant_, supertonic_)
h_I_coup_mel = dominant_4 + Harmony(tonic, mediant | dominant | (tonic + 12))

### Accompaniment
h_I_coup_acc = dominant_3 + Harmony(tonic | mediant, tonic - 12 | tonic)
h_theme_B2_acc = dominant_3 + Harmony(silence, dominant_, submediant_, leading_tone_, tonic, supertonic, mediant, subdominant, dominant, submediant, leading_tone)

## Development
### Melody
h_dev_1 = tonic_4 + Harmony(dominant, led_submediant, submediant, subdominant, supertonic, tonic)
h_dev_2 = tonic_4 + Harmony(leading_tone_)
h_dev_3 = tonic_4 + Harmony(tonic, supertonic, leading_tone_, mediant)
h_dev_tail_1 = tonic_4 + Harmony(dominant, subdominant, mediant, supertonic)
h_dev_tail_2 = tonic_5 + Harmony(dominant, subdominant, mediant, supertonic, tonic, leading_tone_, submediant_, dominant_, subdominant_, mediant_, supertonic_)

## Theme P prime
### Melody
h_theme_A_1_prime = h_theme_A_1
h_theme_A_2_prime = tonic_4 + Harmony(dominant, mediant + 12, supertonic + 12, tonic + 12, leading_tone, submediant)
h_theme_P_prime_3 = tonic_4 + Harmony(supertonic, mediant, subdominant, supertonic)
h_theme_P_prime_4 = tonic_4 + Harmony(submediant, dominant, mediant, tonic)
h_theme_P_prime_5 = tonic_4 + Harmony(supertonic, mediant, supertonic, led_supertonic, supertonic, mediant, subdominant)
h_theme_P_prime_6 = tonic_4 + Harmony(submediant, dominant, mediant, subdominant, supertonic)
h_theme_P_prime_cad_1 = tonic_4 + Harmony(tonic, tonic | mediant, leading_tone_ | supertonic)
h_theme_P_prime_cad_2 = tonic_4 + Harmony(tonic, dominant, dominant)

### Accompaniment
h_theme_P_acc_1 = tonic_3 + Harmony(tonic, dominant, mediant, subdominant, submediant)
h_theme_P_acc_2 = tonic_3 + Harmony(dominant_, dominant, led_dominant, subdominant, dominant)


# Structure
## Theme P
### Melody
melody_1 = ((t_theme_A_head * t_3_quarters @ h_theme_A_1) *
            (t_theme_A_head * t_half_quarter @ h_theme_A_2) *
            (t_theme_A_head * t_6_eighths @ h_theme_A_3) *
            (t_3_quarters * t_half_quarter @ h_theme_A_4))

### Accompaniment
accompaniment_1 = ((t_alberti_1 ** 2 @ ((tonic_3 + h_I) * 2)) *
                   (t_alberti_1 ** 2 @ ((tonic_3 + h_I) + (tonic_3 + h_V34))) *
                   (t_alberti_1 ** 2 @ ((tonic_3 + h_V6) + (tonic_3 + h_I))) *
                   (t_alberti_2_a * t_alberti_2_b * t_alberti_cad @ ((tonic_3 + h_V34) + (tonic_3 + h_Ino3) + (tonic_3 + h_V_prime))))

theme_p = accompaniment_1 + melody_1


## Theme S
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
accompaniment_2 = ((t_acc_B_head @ (dominant_4 + h_Ino5.flat())) *
                   (t_acc_B_tail @ (dominant_4 + h_viino5.flat())) *
                   (t_acc_B_head @ (dominant_4 + h_vii.flat())) *
                   (t_acc_B_tail @ (dominant_4 + h_Ino5.flat())) *
                   (t_acc_B_head @ (dominant_4 + h_Ino1.flat())) *
                   (t_acc_B_tail_prime @ (dominant_4 + h_IVno5.flat())) *
                   (t_cad_1 @ (dominant_4 + h_dom8)) *
                   (t_coup @ (dominant_3 + reversed(h_ton8))) *
                   (t_theme_B2_4 @ h_theme_B2_acc) *
                   (t_eighth_full @ (dominant_4 + h_ton)) *
                   (t_dotted_half @ (dominant_3 + h_V7no35.flat())) *
                   (t_coup @ h_I_coup_acc))

theme_s = melody_2 + accompaniment_2

## Development
### Melody
mel_dev_head = ((t_6_eighths @ h_dev_1) *
              (t_3_quarter_p @ h_dev_2) *
              (t_dev_3 @ h_dev_3))
mel_dev_tail_1 = t_dev_4 @ h_dev_tail_1
mel_dev_tail_2 = t_theme_B2_4 @ h_dev_tail_2

### Accompaniment
acc_dev_head = ((t_dotted_half @ h_silence) *
                (t_acc_B_head @ (tonic_3 + h_V7no3.flat())) *
                (t_3_quarter_p @ (tonic_3 + h_I46.flat())))
acc_dev_tail_1 = t_dotted_half @ (tonic_3 + h_V.flat())
acc_dev_tail_2 = t_quarter @ (tonic_4 + h_V.flat())

development_head = mel_dev_head + acc_dev_head
development_tail_1 = mel_dev_tail_1 + acc_dev_tail_1
development_tail_2 = mel_dev_tail_2 + acc_dev_tail_2

developpement = development_head * development_tail_1 * ((development_head + 12) * development_tail_2)

## Theme P prime
melody_1_prime_head = ((t_theme_A_head * t_3_quarters @ h_theme_A_1_prime) *
                  (t_theme_A_head * t_half_quarter @ h_theme_A_2_prime))

melody_1_prime_mid = ((t_theme_A_head @ h_theme_P_prime_3) *
                      (t_theme_A_head @ h_theme_P_prime_4))

melody_1_prime_tail = ((t_theme_P_prime_1 @ h_theme_P_prime_5) *
                       (t_theme_P_prime_2 @ h_theme_P_prime_6))

melody_1_prime_cad = (t_3_quarters @ h_theme_P_prime_cad_1) * (t_3_quarters @ h_theme_P_prime_cad_2)

melody_1_prime = melody_1_prime_head * melody_1_prime_mid * (melody_1_prime_mid + 12) * melody_1_prime_tail * melody_1_prime_cad

accompaniment_1_prime = ((t_alberti_1 @ (tonic_3 + h_I)) ** 3 *
                         (t_alberti_1 @ (tonic_3 + h_IV_46)) *
                         (t_alberti_1 ** 2 @ (tonic_3 + (h_V56 + h_I))) ** 2 *
                         (t_alberti_1 @ (tonic_3 + h_V56)) *
                         (t_alberti_3 @ h_theme_P_acc_1) *
                         (t_alberti_3 @ h_theme_P_acc_2) *
                         (t_quarter_full @ (tonic_3 + h_Ino5.flat())))

theme_p_prime = accompaniment_1_prime + melody_1_prime

## Theme S prime
theme_s_prime = theme_s + 5


## Full piece
piece = (theme_p * theme_s * developpement * theme_p_prime * theme_s_prime) @ piano

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
