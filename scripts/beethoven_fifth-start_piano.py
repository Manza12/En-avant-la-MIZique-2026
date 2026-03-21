from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument, Section
from musictensors.plot import plot_notes, plt
from musictensors import frac

# =============================================================================
# TONIC
# =============================================================================
C4 = Pitch(60)

# Octaves
octave_4 = C4
octave_3 = C4 - 12
octave_2 = C4 - 12 * 2
octave_1 = C4 - 12 * 3
octave_5 = C4 + 12
octave_6 = C4 + 12 * 2

# =============================================================================
# TEXTURES
# =============================================================================

t_main_head = Texture(
    Rhythm(Hit('1/8', '1/8'), Hit('2/8', '1/8'), Hit('3/8', '1/8'))
)
t_main_head_bis = Texture(
    Rhythm(Hit('1/8', '1/8'), Hit('2/8', '1/8')),
    Rhythm(Hit('3/8', '1/8'))
)
t_main_head_ter = Texture(
    Rhythm(Hit('1/8', '1/8')),
    Rhythm(Hit('2/8', '1/8')),
    Rhythm(Hit('3/8', '1/8'))
)
t_half = Texture(Rhythm(Hit('0', '1/2')))

t_main_1 = t_main_head * t_half
t_main_2 = t_main_head * (t_half * frac(2))

r_quarter = Rhythm(Hit('0', '1/4'))

# =============================================================================
# ORCHESTRATION
# =============================================================================

flute      = Instrument('Flute')
oboe       = Instrument('Oboe')
clarinet   = Instrument('Clarinet')
basson     = Instrument('Bassoon')
horn       = Instrument('French Horn')
trombone   = Instrument('Trombone')
timpani    = Instrument('Timpani')
violin     = Instrument('Violin')
viola      = Instrument('Viola')
cello      = Instrument('Cello')
contrabass = Instrument('Contrabass')
piano      = Instrument('Acoustic Grand Piano')

s_violin     = Section(violin)
s_clarinet   = Section(clarinet)
s_viola      = Section(viola)
s_cello      = Section(cello)
s_contrabass = Section(contrabass)
s_basson     = Section(basson)
s_trombone   = Section(trombone)
s_horn       = Section(horn)
s_timpani    = Section(timpani)
s_flute      = Section(flute)
s_oboe       = Section(oboe)
s_piano      = Section(piano)

s_1_high = Section(clarinet, violin)
s_1_medi = Section(viola)
s_1_bass = Section(cello)
s_1_dbas = Section(contrabass)

s_all = Section(violin, viola, cello, contrabass,
                flute, oboe, clarinet, basson,
                horn, trombone, timpani)

# =============================================================================
# HARMONY
# =============================================================================

tonic        = Chord({0})
supertonic   = Chord({2})
mediant      = Chord({3})
subdominant  = Chord({5})
tritone      = Chord({6})
dominant     = Chord({7})
submediant   = Chord({8})
leading_tone = Chord({11})

supertonic_  = supertonic  - 12
mediant_     = mediant     - 12
subdominant_ = subdominant - 12
tritone_     = tritone     - 12
dominant_    = dominant    - 12
submediant_  = submediant  - 12
leading_tone_= leading_tone- 12

h_1 = Harmony(dominant, mediant)
h_2 = Harmony(subdominant, supertonic)
h_3 = Harmony(submediant, dominant)
h_4 = Harmony(mediant, tonic)
h_5 = Harmony(dominant, supertonic)
h_6 = Harmony(dominant, subdominant, mediant)
h_6_ = reversed(h_6)

h_ton  = Harmony(Chord({0}))
h_led_ = Harmony(Chord({-1}))

# =============================================================================
# PHRASE 1
# =============================================================================

# m_1_high = (t_main_1 @ (octave_4 + h_1)) @ s_1_high
# m_1_medi = (t_main_1 @ (octave_3 + h_1)) @ s_1_medi
# m_1_bass = (t_main_1 @ (octave_2 + h_1)) @ s_1_bass
# m_1_dbas = (t_main_1 @ (octave_1 + h_1)) @ s_1_dbas
m_1_piano = (t_main_1 @ (octave_3 + h_1)) @ s_piano
m_1 = m_1_piano  # m_1_high + m_1_medi + m_1_bass + m_1_dbas

# m_2_high = (t_main_2 @ (octave_4 + h_2)) @ s_1_high
# m_2_medi = (t_main_2 @ (octave_3 + h_2)) @ s_1_medi
# m_2_bass = (t_main_2 @ (octave_2 + h_2)) @ s_1_bass
# m_2_dbas = (t_main_2 @ (octave_1 + h_2)) @ s_1_dbas
m_2_piano = (t_main_2 @ (octave_3 + h_2)) @ s_piano
m_2 = m_2_piano  # m_2_high + m_2_medi + m_2_bass + m_2_dbas

phrase_1 = m_1 * m_2

# =============================================================================
# FULL PIECE
# =============================================================================

piece = phrase_1

# # Transport the contrabass part to the actual range of the instrument
# for note in piece.notes():
#     if note.instrument.name == 'Contrabass':
#         note.pitch.number -= 12

# =============================================================================
# PATHS & RENDER
# =============================================================================

name = 'beethoven_fifth-start_piano'
midi_path  = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

midi = piece.to_midi(bpm=108 * 2)
midi.write(midi_path)

render_midi_to_audio(midi_path, audio_path, sf2_path)

plot_notes(piece, figsize=(6, 2), x_tick_start=0, x_tick_step=frac(1, 2))  # , color_by_instrument=True
# Save the plot as a vector image (SVG)
plt.savefig(f'../plots/{name}.svg', format='svg')
plt.show()