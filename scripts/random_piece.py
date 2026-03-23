from pathlib import Path
from fractions import Fraction
import random

from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Instrument, Section
from musictensors.plot import plot_notes, plt
from musictensors.audio import render_midi_to_audio, sf2_path

# =============================================================================
# PARAMETERS
# =============================================================================

SEED = 42
random.seed(SEED)

# Texture
N_RHYTHMS   = 32      # number of Rhythms in the Texture
N_HITS_MIN  = 1      # hits per Rhythm
N_HITS_MAX  = 1

# Hits
ONSET_MIN    = 0
ONSET_MAX    = 128     # within one bar
DURATION_MIN = 1
DURATION_MAX = 32
DENOMINATOR = 32

# Harmony
N_CHORDS      = N_RHYTHMS      # one chord per rhythm
N_NOTES_MIN   = 1              # notes per chord
N_NOTES_MAX   = 1
PITCH_MIN     = 48             # C3
PITCH_MAX     = 72             # C5

# Orchestration
N_SECTIONS    = N_RHYTHMS      # one section per rhythm
INSTRUMENTS   = ['Violin', 'Flute', 'Acoustic Grand Piano', 'Trumpet']
N_INSTR_MIN   = 1              # instruments per section
N_INSTR_MAX   = 1

# Repetitions & render
N_BARS  = 1
BPM     = 120

# =============================================================================
# RANDOM HELPERS
# =============================================================================

def rand_frac(lo: int, hi: int) -> Fraction:
    num = random.randint(lo, hi)
    return Fraction(num, DENOMINATOR)

def rand_hit() -> Hit:
    onset    = rand_frac(ONSET_MIN, ONSET_MAX)
    duration = rand_frac(DURATION_MIN, DURATION_MAX)
    return Hit(onset, duration)

def rand_rhythm() -> Rhythm:
    n = random.randint(N_HITS_MIN, N_HITS_MAX)
    return Rhythm(*[rand_hit() for _ in range(n)])

def rand_chord() -> Chord:
    n = random.randint(N_NOTES_MIN, N_NOTES_MAX)
    pitches = {random.randint(PITCH_MIN, PITCH_MAX) for _ in range(n)}
    return Chord(pitches)

def rand_section() -> Section:
    n = random.randint(N_INSTR_MIN, N_INSTR_MAX)
    instruments = [Instrument(random.choice(INSTRUMENTS)) for _ in range(n)]
    return Section(*instruments)

# =============================================================================
# GENERATE RANDOM TEXTURE, HARMONY, ORCHESTRATION
# =============================================================================

texture = Texture(*[rand_rhythm() for _ in range(N_RHYTHMS)])
harmony = Harmony(*[rand_chord()  for _ in range(N_CHORDS)])

# One ScoreTensor per section (one per rhythm slot)
harmonic_texture = texture @ harmony

bars = []
for _ in range(N_BARS):
    # Re-randomise harmony and orchestration each bar for variety
    harmony_bar = Harmony(*[rand_chord()  for _ in range(N_CHORDS)])
    section_bar = [rand_section() for _ in range(N_RHYTHMS)]

    # Apply harmony, then assign each rhythm slot to its section
    ht = texture @ harmony_bar
    # Build bar as sum of individual rhythm@section pairs
    bar = None
    for i, section in enumerate(section_bar):
        # Slice the i-th rhythm and its chord
        ht_i = Texture(texture.rhythms[i]) @ Harmony(harmony_bar.chords[i])
        part = ht_i @ section
        bar = part if bar is None else bar + part
    bars.append(bar)

# Concatenate bars
piece = bars[0]
for b in bars[1:]:
    piece = piece * b

# =============================================================================
# RENDER
# =============================================================================

name       = 'random_piece'
midi_path  = Path(f'../midi/{name}.mid')
audio_path = Path(f'../audio/{name}.wav')

midi = piece.to_midi(bpm=BPM)
midi.write(midi_path)

render_midi_to_audio(midi_path, audio_path, sf2_path)

# =============================================================================
# PLOT
# =============================================================================

plot_notes(piece,
           figsize=(9, 4),
           x_tick_start=0,
           x_tick_step=Fraction(1, 4),
           color_by_instrument=True)
plt.savefig(f'../plots/{name}.svg', format='svg')
plt.show()