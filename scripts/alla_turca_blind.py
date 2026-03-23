from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path
from musictensors.model import Hit, Harmony, Chord, Rhythm, Texture, Pitch, Instrument
from musictensors.plot import plot_notes, plt

# =============================================================================
# TONIC
# =============================================================================

A4 = Pitch(69)   # melody tonic  (outer activation freq=69)
A3 = Pitch(57)   # harmony tonic (outer activation freq=57)

# =============================================================================
# TEXTURES
# =============================================================================

# Texture 1 — melody motif with anacrusis (negative onsets)
texture_1 = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('0', '1/4')),
)
t_quarter = Texture(Rhythm(Hit('0', '1/4')))

# Texture 2 — accompaniment arpeggio
texture_2 = Texture(
    Rhythm(Hit('0', '1/2')),
    Rhythm(Hit('0', '1/2')),
)

texture_3 = Texture(
    Rhythm(Hit('0', '1/4')),
    Rhythm(Hit('0', '1/4'))
)

# =============================================================================
# MELODY HARMONIES  (relative to A4 = Pitch(69))
# =============================================================================

melody_1 = Harmony(
    A4 + Chord({2}),    # B4
    A4 + Chord({0}),    # A4
    A4 + Chord({-1}),   # G#4
    A4 + Chord({3}),    # C5
)

melody_2 = Harmony(
    A4 + Chord({5}),    # D5
    A4 + Chord({3}),    # C5
    A4 + Chord({2}),    # B4
    A4 + Chord({7}),    # E5
)

melody_3 = Harmony(
    A4 + Chord({8}),    # F5
    A4 + Chord({7}),    # E5
    A4 + Chord({6}),    # Eb5
)

melody_4 = Harmony(
    A4 + Chord({2}),    # B4
    A4 + Chord({0}),    # A4
    A4 + Chord({-1}),   # G#4
)

# =============================================================================
# ACCOMPANIMENT HARMONIES  (relative to A3 = Pitch(57))
# =============================================================================

# Group 1: used at time offsets 0/2, 1/2, 3/2
acc_harmony_1 = Harmony(
    A3 + Chord({0}),        # A3
    A3 + Chord({3, 7}),     # C4 + E4
)

# =============================================================================
# INSTRUMENT
# =============================================================================

piano = Instrument('Acoustic Grand Piano')

# =============================================================================
# MELODY SECTIONS
# Activation table says the melody component appears at:
#   (t=0/2, f=0), (t=3/2, f=+12)  → mel-1
#   (t=1/2, f=0)                   → mel-2
#   (t=2/2, f=0)                   → mel-3
#   (t=5/4, f=+12)                 → mel-4
#
# We ignore the activation shifts and just concatenate/parallelise
# in a musically reasonable order.
# =============================================================================

mel_1 = (texture_1 * t_quarter @ melody_1) @ piano
mel_2 = (texture_1 * t_quarter @ melody_2) @ piano
mel_3 = (texture_1 * texture_1 @ (melody_3 + (melody_4 + 12))) @ piano
mel_4 = (texture_1 * t_quarter @ (melody_1 + 12)) @ piano

# Melodic phrase A: mel_1 * mel_2 (first half)
# Melodic phrase B: mel_3 * mel_4 (second half, ends on rest)
melody_phrase_a = mel_1 * mel_2
melody_phrase_b = mel_3 * mel_4
melody = melody_phrase_a * melody_phrase_b * (texture_3 @ (A4 + Harmony(Chord({12}), Chord({15}))) @ piano)

# =============================================================================
# ACCOMPANIMENT SECTIONS
# Activation table says acc group 1 appears 3 times, group 2 appears 2 times
# Reasonable layout: 1 1 2 1 2
# =============================================================================

acc_1a = (texture_2 @ acc_harmony_1) @ piano
acc_1b = (texture_2 @ acc_harmony_1) @ piano
acc_2a = ((texture_3 @ acc_harmony_1) ** 2) @ piano
acc_1c = (texture_2 @ acc_harmony_1) @ piano

accompaniment = (t_quarter @ Harmony(Chord()) @ piano) * acc_1a * acc_1b * acc_2a * acc_1c

# Phrase 2
h_1 = Harmony(
    A4 + Chord({14}),
    A4 + Chord({9, 12}),
    A4 + Chord({7, 10}),
    A4 + Chord({9, 12}),
)
h_2 = Harmony(
    A4 + Chord({14}),
    A4 + Chord({9, 12}),
    A4 + Chord({7, 10}),
    A4 + Chord({6, 9}),
)

h_3 = Harmony(
    A3 + Chord({-5}),
    A3 + Chord({2, 7})
)

h_4 = Harmony(
    A3 + Chord({-10}),
    A3 + Chord({2})
)

phrase_2_mel = (texture_3 ** 2 @ h_1) * (texture_3 ** 2 @ h_1) * (texture_3 ** 2 @ h_2) * (t_quarter @ (A4 + Harmony(Chord({7})))) @ piano
phrase_2_acc = (texture_2 @ h_3) * (texture_2 @ h_3) * (texture_3 @ h_3) * (texture_3 @ h_4) * (t_quarter @ (A3 + Harmony(Chord({-5})))) @ piano

phrase_2 = phrase_2_mel + phrase_2_acc

# =============================================================================
# FULL PIECE  — melody and accompaniment in parallel
# =============================================================================

piece = (melody + accompaniment) * phrase_2

# =============================================================================
# RENDER
# =============================================================================

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