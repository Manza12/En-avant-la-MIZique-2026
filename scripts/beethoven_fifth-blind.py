from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument, Section
from musictensors.plot import plot_notes, plt
from musictensors import frac, Orchestration

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

t_main_1 = Texture(Rhythm(Hit('0', '1')), Rhythm(Hit('0', '1')))
t_main_2 = Texture(Rhythm(Hit('0', '3/2')), Rhythm(Hit('0', '3/2')))

r_quarter = Rhythm(Hit('0', '1/4'))

# =============================================================================
# ORCHESTRATION
# =============================================================================

flute      = Instrument('Acoustic Grand Piano')
oboe       = Instrument('Acoustic Grand Piano')
clarinet   = Instrument('Acoustic Grand Piano')
basson     = Instrument('Acoustic Grand Piano')
horn       = Instrument('Acoustic Grand Piano')
trombone   = Instrument('Acoustic Grand Piano')
timpani    = Instrument('Acoustic Grand Piano')
violin     = Instrument('Acoustic Grand Piano')
viola      = Instrument('Acoustic Grand Piano')
cello      = Instrument('Acoustic Grand Piano')
contrabass = Instrument('Acoustic Grand Piano')

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

m_1_high = (t_main_1 @ (octave_4 + h_1)) @ s_1_high
m_1_medi = (t_main_1 @ (octave_3 + h_1)) @ s_1_medi
m_1_bass = (t_main_1 @ (octave_2 + h_1)) @ s_1_bass
m_1_dbas = (t_main_1 @ (octave_1 + h_1)) @ s_1_dbas
m_1 = m_1_high + m_1_medi + m_1_bass + m_1_dbas

m_2_high = (t_main_2 @ (octave_4 + h_2)) @ s_1_high
m_2_medi = (t_main_2 @ (octave_3 + h_2)) @ s_1_medi
m_2_bass = (t_main_2 @ (octave_2 + h_2)) @ s_1_bass
m_2_dbas = (t_main_2 @ (octave_1 + h_2)) @ s_1_dbas
m_2 = m_2_high + m_2_medi + m_2_bass + m_2_dbas

phrase_1 = m_1 * m_2

# =============================================================================
# PHRASE 2
# =============================================================================

cello_basson = Section(cello, basson)

t_half = Texture(Rhythm(Hit('0', '1/2')))

ot_1 = ((t_half * frac(3*4+1+2, 4))*2) @ (s_violin * 2)
ot_2 = (((t_half * frac(2*4+2+2, 4))*2) + frac(1, 2)) @ (s_viola * 2)
ot_3 = (((t_half * frac(1*4+2+2, 4))*2) + frac(2, 2)) @ (s_violin * 2)
ot_high = ot_1 + ot_2 + ot_3
ot_bass  = (t_half * frac(4) + frac(1, 2)) @ cello_basson
ot = ot_high + ot_bass

h_I = octave_4 + (h_1 + h_3 + (h_4 + 12) + h_ton)
h_V = octave_4 + (h_5 + h_3 + (h_2 + 12) + h_led_)

phrase_2 = (ot @ h_I) * ((ot @ h_V) + frac(-1, 2))
phrase_2.end = frac(4)

# =============================================================================
# PHRASE 3
# =============================================================================

t_ph3 = t_half * frac(2, 1)

m_4 = ((t_ph3 @ (octave_4 + h_6)) @ (s_violin * 3)) + \
      ((t_half + frac(1, 2)) @ (octave_4 + h_ton) @ cello_basson)
m_5 = ((t_ph3 @ (octave_4 + h_6_)) @ (Section(violin, viola) * 3)) + \
      ((t_half + frac(1, 2)) @ (octave_4 + h_led_) @ cello_basson)

m_6 = m_4 * (m_5 + frac(-1, 2))
phrase_3 = m_6 * (m_6 + frac(-2, 2))
phrase_3.end = frac(2)

# =============================================================================
# PHRASE 4
# =============================================================================

h_flauti = octave_6 + (Harmony(supertonic | dominant) + Harmony(supertonic | subdominant))
m_1_flauti = t_half @ h_flauti @ (Section(flute) * 2)

h_oboi = octave_5 + (Harmony(supertonic | dominant) + Harmony(supertonic | subdominant))
m_1_oboi = t_half @ h_oboi @ (Section(oboe) * 2)

h_clarinet = octave_4 + (Harmony(dominant_ | leading_tone_) + Harmony(leading_tone_ | supertonic) + Harmony(supertonic | dominant))
m_1_clarinet = t_half @ h_clarinet @ (Section(clarinet) * 3)

h_basson = octave_3 + Harmony(leading_tone_)
m_1_basson = t_half @ h_basson @ (Section(basson) * 1)

h_horn = octave_3 + Harmony(dominant)
m_1_horn = t_half @ h_horn @ (Section(horn) * 1)

h_trombone = octave_3 + Harmony(dominant_ | dominant)
m_1_trombone = t_half @ h_trombone @ (Section(trombone) * 1)

h_timpani = octave_2 + Harmony(dominant)
m_1_timpani = t_half @ h_timpani @ (Section(timpani) * 1)

h_violin = octave_5 + (Harmony(supertonic | dominant) + Harmony(dominant_ | subdominant))
m_1_violin = t_half @ h_violin @ (Section(violin) * 2)

h_cello = octave_3 + h_led_
m_1_cello = t_half @ h_cello @ (Section(cello) * 1)

h_contrabass = octave_2 + h_led_
m_1_contrabass = t_half @ h_contrabass @ (Section(contrabass) * 1)

m_1 = (m_1_flauti +
    m_1_oboi +
    m_1_clarinet +
    m_1_basson +
    m_1_horn +
    m_1_trombone +
    m_1_timpani +
    m_1_violin +
    m_1_cello +
    m_1_contrabass)

h_2 = ((octave_2 + Harmony(tonic)) +  # Contrabass
       (octave_3 + Harmony(tonic)) +  # Cello
       (octave_3 + Harmony(mediant)) +  # Viola
       (octave_3 + Harmony(tonic | dominant | (mediant + 12))) +  # Violin
       (octave_2 + Harmony(tonic)) +  # Timpani
       (octave_2 + Harmony(tonic | (tonic + 12))) +  # Trombone
       (octave_3 + Harmony(dominant)) +  # Horn
       (octave_3 + Harmony(tonic)) +  # Bassoon
       (octave_3 + Harmony(mediant | dominant)) +  # Clarinet
       (octave_5 + Harmony(tonic | mediant)) +  # Oboe
       (octave_6 + Harmony(tonic | mediant)))  # Flute

o_2 = Orchestration(s_contrabass, s_cello, s_viola, s_violin, s_timpani, s_trombone, s_horn, s_basson, s_clarinet, s_oboe, s_flute)
t_2 = Texture(*(r_quarter for _ in range(11)))
m_2 = t_2 @ h_2 @ o_2


h_3 = ((octave_2 + Harmony(submediant_)) +  # Contrabass
       (octave_2 + Harmony(submediant_)) +  # Cello
       (octave_3 + Harmony(submediant_)) +  # Viola
       (octave_3 + Harmony(submediant_ | tritone | (tonic + 12))) +  # Violin
       (octave_2 + Harmony(tonic)) +  # Timpani
       (octave_2 + Harmony(tonic | (tonic + 12))) +  # Trombone
       (octave_3 + Harmony(mediant | mediant_)) +  # Horn
       (octave_2 + Harmony(submediant_)) +  # Bassoon
       (octave_3 + Harmony(tonic | tritone)) +  # Clarinet
       (octave_5 + Harmony(tonic | tritone)) +  # Oboe
       (octave_6 + Harmony(tonic)))  # Flute

m_3 = t_2 @ h_3 @ o_2


h_4 = ((octave_2 + Harmony(dominant)) +  # Contrabass
       (octave_2 + Harmony(dominant)) +  # Cello
       (octave_3 + Harmony(dominant)) +  # Viola
       (octave_3 + Harmony(dominant_ | dominant | leading_tone)) +  # Violin
       (octave_2 + Harmony(dominant_)) +  # Timpani
       (octave_2 + Harmony(dominant_ | dominant)) +  # Trombone
       (octave_3 + Harmony(dominant_ | dominant)) +  # Horn
       (octave_2 + Harmony(dominant_)) +  # Bassoon
       (octave_3 + Harmony(leading_tone_ | supertonic)) +  # Clarinet
       (octave_5 + Harmony(leading_tone_ | dominant)) +  # Oboe
       (octave_6 + Harmony(leading_tone_ | dominant)))  # Flute

m_4 = t_2 @ h_4 @ o_2

quarter_silence = Texture(Rhythm(Hit('0', '1/4'))) @ Harmony(Chord()) @ s_all

phrase_4 = m_1 * m_2 * quarter_silence * m_3 * quarter_silence * m_4 * quarter_silence

# =============================================================================
# FULL PIECE
# =============================================================================

piece = phrase_1 * phrase_2 * phrase_3 * phrase_4

# # Transport the contrabass part to the actual range of the instrument
# for note in piece.notes():
#     if note.instrument.name == 'Contrabass':
#         note.pitch.number -= 12

# =============================================================================
# PATHS & RENDER
# =============================================================================

name = Path(__file__).stem
midi_path  = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

midi = piece.to_midi(bpm=108 * 2)
midi.write(midi_path)

render_midi_to_audio(midi_path, audio_path, sf2_path)

plot_notes(piece, figsize=(12, 6), x_tick_start=0, x_tick_step=1, color_by_instrument=True)
plt.show()