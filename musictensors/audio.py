import subprocess
from pathlib import Path


def render_midi_to_audio(midi_path, wav_path, soundfont, sample_rate=48000):
    """
    Render a MIDI file to audio using FluidSynth.

    Parameters
    ----------
    midi_path : str or Path
    wav_path : str or Path
    soundfont : str or Path
    sample_rate : int
    """

    midi_path = Path(midi_path)
    wav_path = Path(wav_path)
    soundfont = Path(soundfont)

    wav_path.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        "fluidsynth",
        "-ni",
        "-F", str(wav_path),
        "-r", str(sample_rate),
        str(soundfont),
        str(midi_path)
    ], check=True)
