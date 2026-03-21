import subprocess
from pathlib import Path


sound_fonts_paths = {
    'FluidR3_GM2-2': Path("../../../SoundFonts/FluidR3_GM2-2.sf2"),
    'GeneralUser':   Path("../../../SoundFonts/GeneralUser-GS/GeneralUser-GS.sf2"),
    'Musyng Kite':   Path("../../../SoundFonts/Musyng_Kite/Musyng_Kite.sf2"),
    'Arachno':       Path("../../../SoundFonts/Arachno/Arachno-v1.0.sf2"),
    'Timbres of Heaven': Path("../../../SoundFonts/Timbres_of_Heaven/Timbres of Heaven (XGM) 4.00(G).sf2"),
}
sf2_path = sound_fonts_paths['Timbres of Heaven']


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
