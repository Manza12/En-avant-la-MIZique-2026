from pathlib import Path
from time import time

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument
from musictensors.plot import plot_notes, plt

start = time()

# =============================================================================
# TONIC
# =============================================================================
E4 = Pitch(64)

# ==============#
# SCALE DEGREES #
# ==============#

tonic        = Chord({0})
supertonic   = Chord({2})
mediant      = Chord({3})
subdominant  = Chord({5})
dominant     = Chord({7})
submediant   = Chord({8})
leading_tone = Chord({11})
subtonic     = Chord({10})

# Chromatic degrees
flat_second  = Chord({1})
flat_third   = Chord({3})
tritone      = Chord({6})
sharp_sixth  = Chord({9})

# ============== #
# OCTAVE HELPERS #
# ============== #

def up(chord, n=1):
    return chord + 12 * n

def down(chord, n=1):
    return chord - 12 * n

# One octave below (for convenience)
tonic_1        = down(tonic)
supertonic_1   = down(supertonic)
mediant_1      = down(mediant)
subdominant_1  = down(subdominant)
dominant_1     = down(dominant)
submediant_1   = down(submediant)
leading_tone_1 = down(leading_tone)

flat_third_1   = down(flat_third)
sharp_sixth_1  = down(sharp_sixth)
subtonic_1     = down(subtonic)

# Two octaves below
tonic_2        = down(tonic, 2)
supertonic_2   = down(supertonic, 2)
dominant_2     = down(dominant, 2)
subdominant_2  = down(subdominant, 2)
tritone_2      = down(tritone, 2)
sharp_sixth_2  = down(sharp_sixth, 2)

# ======= #
# TEXTURE #
# ======= #

R_1 = Rhythm(Hit('0/4', '1/4'))
R_2 = Rhythm(Hit('1/4', '1/4'))
R_3 = Rhythm(Hit('2/4', '1/4'))
R_4 = Rhythm(Hit('0', '5/4'))
R_5 = Rhythm(Hit('0', '1/2'), Hit('1/2', '3/4'))
R_6 = Rhythm(Hit('0', '1'))

t_head = Texture(R_1, R_2, R_3)
t_1 = t_head * Texture(R_4)
t_2 = t_head * Texture(R_5)
t_3 = t_head * Texture(R_6)

t_bass = Texture(R_6)

# ========== #
# INSTRUMENT #
# ========== #

piano = Instrument('Acoustic Grand Piano')
saxo = Instrument('Alto Sax')

# ======= #
# HARMONY #
# ======= #
# Octaves
octave_4 = E4
octave_3 = E4 - 12
octave_2 = E4 - 12 * 2
octave_5 = E4 + 12
octave_6 = E4 + 12 * 2

# ========= #
# STRUCTURE #
# ========= #

# === Melody === #
h_0 = Harmony(Chord())
m_0 = (Texture(R_1) @ h_0) @ saxo

h_1 = octave_4 + Harmony(tonic, supertonic, mediant, submediant)
m_1 = (t_1 @ h_1) @ saxo

h_2 = octave_4 + Harmony(subtonic_1, tonic, supertonic, dominant)
m_2 = (t_2 @ h_2) @ saxo

h_3 = octave_4 + Harmony(submediant_1, subtonic_1, tonic, subdominant)
m_3 = (t_1 @ h_3) @ saxo

h_4 = octave_4 + Harmony(dominant_1, sharp_sixth_1, leading_tone_1, mediant)
m_4 = (t_3 @ h_4) @ saxo

h_5 = octave_4 + Harmony(supertonic, subdominant, mediant, tonic)
m_5 = (t_1 @ h_5) @ saxo

melody = m_0 * m_1 * m_2 * m_3 * m_4 * m_0 * m_1 * m_2 * m_3 * m_5

# === Accompaniment === #
h_0 = Harmony(Chord())
m_0 = (t_bass @ h_0) @ piano

h_1 = octave_3 + Harmony(subdominant | submediant | tonic | mediant)
m_1 = (t_bass @ h_1) @ piano

h_2 = octave_3 + Harmony(subtonic_1 | supertonic | subdominant | submediant)
m_2 = (t_bass @ h_2) @ piano

h_3 = octave_3 + Harmony(mediant | dominant | subtonic | supertonic)
m_3 = (t_bass @ h_3) @ piano

h_4 = octave_3 + Harmony(submediant_1 | tonic | mediant | dominant)
m_4 = (t_bass @ h_4) @ piano

h_5 = octave_3 + Harmony(supertonic | subdominant | submediant | tonic)
m_5 = (t_bass @ h_5) @ piano

h_6 = octave_3 + Harmony(dominant_1 | leading_tone_1 | supertonic | subdominant)
m_6 = (t_bass @ h_6) @ piano

h_7 = octave_3 + Harmony(tonic | mediant | dominant)
m_7 = (t_bass @ h_7) @ piano

accompaniment = (m_0 * m_1 * m_2 * m_3 * m_4 * m_5 * m_6 * m_7) ** 2

# =============================================================================
# FULL PIECE
# =============================================================================


piece = melody + accompaniment

end = time()
print(f"Generated piece in {end - start:.3f} seconds")

# =============================================================================
# RENDER
# =============================================================================

name = Path(__file__).stem
midi_path  = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')
midi_path_accompaniment = Path(f'../midi/{name}-accompaniment.mid')
audio_path_accompaniment = Path(f'../audio/{name}-accompaniment.wav')

midi = piece.to_midi(bpm=90*2)
midi.write(midi_path)

midi_accompaniment = accompaniment.to_midi(bpm=90*2)
midi_accompaniment.write(midi_path_accompaniment)

render_midi_to_audio(midi_path, audio_path, sf2_path)
render_midi_to_audio(midi_path_accompaniment, audio_path_accompaniment, sf2_path)

plot_notes(piece, figsize=(9, 4), x_tick_start=0, x_tick_step=1)
plt.show()