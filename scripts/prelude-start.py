from pathlib import Path
from time import time

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument
from musictensors.plot import plot_notes, plt

start = time()

# =============================================================================
# TONIC
# =============================================================================
C4 = Pitch(60)

# =============================================================================
# SCALE DEGREES (relative to C4, in semitones)
# =============================================================================

tonic        = Chord({0})    # C
supertonic   = Chord({2})    # D
mediant      = Chord({4})    # E
subdominant  = Chord({5})    # F
dominant     = Chord({7})    # G
submediant   = Chord({9})    # A
leading_tone = Chord({11})   # B

# Chromatic degrees
flat_second  = Chord({1})    # C#/Db
flat_third   = Chord({3})    # Eb
tritone      = Chord({6})    # F#/Gb
flat_sixth   = Chord({8})    # Ab
flat_seventh = Chord({10})   # Bb

# =============================================================================
# OCTAVE HELPERS
# =============================================================================

def up(chord, n=1):
    return chord + 12 * n

def down(chord, n=1):
    return chord - 12 * n

# One octave below (for convenience)
tonic_1        = down(tonic)        # C3  = -12
supertonic_1   = down(supertonic)   # D3  = -10
mediant_1      = down(mediant)      # E3  = -8
subdominant_1  = down(subdominant)  # F3  = -7
dominant_1     = down(dominant)     # G3  = -5
submediant_1   = down(submediant)   # A3  = -3
leading_tone_1 = down(leading_tone) # B3  = -1

flat_third_1   = down(flat_third)   # Eb3 = -9
flat_sixth_1   = down(flat_sixth)   # Ab3 = -4
flat_seventh_1 = down(flat_seventh) # Bb3 = -2

# Two octaves below
tonic_2        = down(tonic, 2)     # C2  = -24
supertonic_2   = down(supertonic,2) # D2  = -22
dominant_2     = down(dominant, 2)  # G2  = -17
subdominant_2  = down(subdominant,2)# F2  = -19
tritone_2      = down(tritone, 2)   # F#2 = -18
flat_sixth_2   = down(flat_sixth,2) # Ab2 = -16

# =============================================================================
# TEXTURE (half bar; repeated twice per bar with ** 2)
#
#   R_1 : bass pedal (left hand, voice 5)   onset 0,    dur 1/2
#   R_2 : inner left hand (voice 6)         onset 1/16, dur 7/16
#   R_3 : low-arpeggio note (right hand)    onsets 2/16 and 5/16
#   R_4 : mid-arpeggio note (right hand)    onsets 3/16 and 6/16
#   R_5 : high-arpeggio note (right hand)   onsets 4/16 and 7/16
# =============================================================================

R_1 = Rhythm(Hit('0',    '1/2'))
R_2 = Rhythm(Hit('1/16', '7/16'))
R_3 = Rhythm(Hit('2/16', '1/16'), Hit('5/16', '1/16'))
R_4 = Rhythm(Hit('3/16', '1/16'), Hit('6/16', '1/16'))
R_5 = Rhythm(Hit('4/16', '1/16'), Hit('7/16', '1/16'))

t = Texture(R_1, R_2, R_3, R_4, R_5)

# =============================================================================
# INSTRUMENT
# =============================================================================

piano = Instrument('Acoustic Grand Piano')

# =============================================================================
# HARMONY BUILDER
# h(bass, inner_left, arp_low, arp_mid, arp_high)
# Each argument is a Chord of semitones relative to C4.
# =============================================================================

def h(ba, mi, a0, a1, a2):
    return Harmony(
        C4 + ba,
        C4 + mi,
        C4 + a0,
        C4 + a1,
        C4 + a2,
    )

# =============================================================================
# HARMONIES — verified note by note against the MusicXML
#
# Semitone reference from C4=0:
#   B3=-1  Bb3=-2  A3=-3  Ab3=-4  G3=-5  F#3=-6  F3=-7
#   E3=-8  Eb3=-9  D3=-10  C3=-12
#   G2=-17  F#2=-18  F2=-19  Ab2=-16  C2=-24
# =============================================================================

#      bass          inner_left     arp_low        arp_mid        arp_high
h1  = h(tonic,        mediant,       dominant,      up(tonic),     up(mediant))      # I - C: C E G C E
h2  = h(tonic,        supertonic,    submediant,    up(supertonic),up(subdominant))  # ii - Dm: C D A D F
h3  = h(leading_tone_1,supertonic,   dominant,      up(supertonic),up(subdominant))  # V7 - G7(no3): B D G D F
h4  = h(tonic,        mediant,       dominant,      up(tonic),     up(mediant))      # I - C: = h1
h5  = h(tonic,        mediant,       submediant,    up(mediant),   up(submediant))   # vi - Am: C E A E A
h6  = h(tonic,        supertonic,    tritone,       submediant,    up(supertonic))   # V/V - D: C D F# A D
h7  = h(leading_tone_1,supertonic,   dominant,      up(supertonic),up(dominant))     # V - G: B D G D G
h8  = h(leading_tone_1,tonic,        mediant,       dominant,      up(tonic))        # I7 - Cmaj7: B C E G C

h9  = h(submediant_1, tonic,         mediant,       dominant,      up(tonic))        # vi7 - Am7: A C E G C
h10 = h(supertonic_1, submediant_1,  supertonic,    tritone,       up(tonic))        # V7/V - D7: D A D F# C
h11 = h(dominant_1,   leading_tone_1,supertonic,    dominant,      leading_tone)     # V - G: G B D G B
h12 = h(dominant_1,   flat_seventh_1,mediant,       dominant,      up(flat_second))  # viiº7/ii - C#dim7: G Bb E G C#

h13 = h(subdominant_1,submediant_1,  supertonic,    submediant,    up(supertonic))   # ii - Dm: F A D A D
h14 = h(subdominant_1,flat_sixth_1,  supertonic,    subdominant,   leading_tone)     # vii°7 - Bdim7: F Ab D F B
h15 = h(mediant_1,    dominant_1,    tonic,         dominant,      up(tonic))        # I - C: E G C G C
h16 = h(mediant_1,    subdominant_1, submediant_1,  tonic,         subdominant)      # IV7 - Fmaj7: E F A C F

h17 = h(supertonic_1, subdominant_1, submediant_1,  tonic,         subdominant)      # ii7 - Dm7: D F A C F
h18 = h(dominant_2,   supertonic_1,  dominant_1,    leading_tone_1,subdominant)      # V7 - G7: G2 D3 G3 B3 F4
h19 = h(tonic_1,      mediant_1,     dominant_1,    tonic,         mediant)          # I - C: C3 E3 G3 C4 E4
h20 = h(tonic_1,      dominant_1,    flat_seventh_1,tonic,         mediant)          # V7/IV - C7: C3 G3 Bb3 C4 E4

h21 = h(subdominant_2,subdominant_1, submediant_1,  tonic,         mediant)          # IV7 - Fmaj7: F2 F3 A3 C4 E4
h22 = h(tritone_2,    tonic_1,       submediant_1,  tonic,         flat_third)       # viiº7/V - F#dim7: F#2 C3 A3 C4 Eb4
h23 = h(flat_sixth_2, subdominant_1, leading_tone_1,tonic,         supertonic)       # viiº7 - Bdim7: Ab2 F3 B3 C4 D4
h24 = h(dominant_2,   subdominant_1, dominant_1,    leading_tone_1,supertonic)       # V7 - G7: G2 F3 G3 B3 D4

h25 = h(dominant_2,   mediant_1,     dominant_1,    tonic,         mediant)          # I - C: G2 E3 G3 C4 E4
h26 = h(dominant_2,   supertonic_1,  dominant_1,    tonic,         subdominant)      # I45 - C45: G2 D3 G3 C4 F4
h27 = h(dominant_2,   supertonic_1,  dominant_1,    leading_tone_1,subdominant)      # V7 - G7: G2 D3 G3 B3 F4
h28 = h(dominant_2,   flat_third_1,  submediant_1,  tonic,         tritone)          # viiº7/V - F#dim7: G2 Eb3 A3 C4 F#4

h29 = h(dominant_2,   mediant_1,     dominant_1,    tonic,         dominant)         # I46 - C: G2 E3 G3 C4 G4
h30 = h(dominant_2,   supertonic_1,  dominant_1,    tonic,         subdominant)      # I45 - C45: G2 D3 G3 C4 F4
h31 = h(dominant_2,   supertonic_1,  dominant_1,    leading_tone_1,subdominant)      # V7 - G7: G2 D3 G3 B3 F4
h32 = h(tonic_2,      tonic_1,       dominant_1,    flat_seventh_1,mediant)          # V7/IV - C7: C2 C3 G3 Bb3 E4

# Bar 33: Fm over C pedal — chromatic dissolution run
# C2 bass, C3 inner, then 14 sixteenth notes: F3 A3 C4 F4 C4 A3 C4 A3 F3 A3 F3 D3 F3 D3
h33 = Harmony(
    C4 + tonic_2,        C4 + tonic_1,
    C4 + subdominant_1,  C4 + submediant_1, C4 + tonic,         C4 + subdominant,
    C4 + tonic,          C4 + submediant_1, C4 + tonic,         C4 + submediant_1,
    C4 + subdominant_1,  C4 + submediant_1, C4 + subdominant_1, C4 + supertonic_1,
    C4 + subdominant_1,  C4 + supertonic_1,
)

# Bar 34: G7 over C pedal — dominant run descending
# C2 bass, B2 inner, then: G4 B4 D5 F5 D5 B4 D5 B4 G4 B4 D4 F4 E4 D4
h34 = Harmony(
    C4 + tonic_2,             C4 + down(leading_tone, 2),
    C4 + dominant,            C4 + leading_tone,
    C4 + up(supertonic),      C4 + up(subdominant),
    C4 + up(supertonic),      C4 + leading_tone,
    C4 + up(supertonic),      C4 + leading_tone,
    C4 + dominant,            C4 + leading_tone,
    C4 + supertonic,          C4 + subdominant,
    C4 + mediant,             C4 + supertonic,
)

# Bar 35: final C major whole note chord with fermata
# C2 + C3 + E4 + G4 + C5
h35 = Harmony(
    C4 + (tonic | tonic_1 | tonic_2 | mediant | dominant | up(tonic)),
)

# =============================================================================
# TEXTURES FOR BARS 33–34 (run) AND 35 (final chord)
# =============================================================================

R_b1 = Rhythm(Hit('0',    '1'))
R_b2 = Rhythm(Hit('1/16', '15/16'))
R_n01 = Rhythm(Hit('2/16',  '1/16'))
R_n02 = Rhythm(Hit('3/16',  '1/16'))
R_n03 = Rhythm(Hit('4/16',  '1/16'))
R_n04 = Rhythm(Hit('5/16',  '1/16'))
R_n05 = Rhythm(Hit('6/16',  '1/16'))
R_n06 = Rhythm(Hit('7/16',  '1/16'))
R_n07 = Rhythm(Hit('8/16',  '1/16'))
R_n08 = Rhythm(Hit('9/16',  '1/16'))
R_n09 = Rhythm(Hit('10/16', '1/16'))
R_n10 = Rhythm(Hit('11/16', '1/16'))
R_n11 = Rhythm(Hit('12/16', '1/16'))
R_n12 = Rhythm(Hit('13/16', '1/16'))
R_n13 = Rhythm(Hit('14/16', '1/16'))
R_n14 = Rhythm(Hit('15/16', '1/16'))

t_run   = Texture(R_b1, R_b2,
                  R_n01, R_n02, R_n03, R_n04, R_n05, R_n06, R_n07,
                  R_n08, R_n09, R_n10, R_n11, R_n12, R_n13, R_n14)

t_final = Texture(Rhythm(Hit('0', '1')))

# =============================================================================
# BAR CONSTRUCTION
# =============================================================================

def compas(harmony):
    return ((t @ harmony) ** 2) @ piano

bars = [compas(hh) for hh in [
    h1,  h2,  h3,  h4,  h5,  h6,  h7,  h8,
    h9,  h10, h11, h12, h13, h14, h15, h16,
    h17, h18, h19, h20, h21, h22, h23, h24,
    h25, h26, h27, h28, h29, h30, h31, h32,
]]

m33 = (t_run   @ h33) @ piano
m34 = (t_run   @ h34) @ piano
m35 = (t_final @ h35) @ piano

# =============================================================================
# FULL PIECE
# =============================================================================

piece = bars[0] * bars[1] * bars[2] * bars[3]

end = time()
print(f"Generated piece in {end - start:.3f} seconds")

# =============================================================================
# RENDER
# =============================================================================

name = Path(__file__).stem
midi_path  = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

start = time()
midi = piece.to_midi(bpm=72, velocity=90)
midi.write(midi_path)
end = time()
print(f"Wrote MIDI in {end - start:.3f} seconds")

start = time()
render_midi_to_audio(midi_path, audio_path, sf2_path)
end = time()
print(f"Rendered audio in {end - start:.3f} seconds")

plot_notes(piece, figsize=(8, 3), x_tick_start=0, x_tick_step=1)
plt.tight_layout()

# Save the plot as a vector image (SVG)
plt.savefig(f'../plots/{name}.svg', format='svg')

plt.show()