from pathlib import Path

from musictensors.audio import render_midi_to_audio, sf2_path

# =========================
# CONFIG
# =========================

BASE_DIR = Path(__file__).parent
SF2_PATH = Path('..') / sf2_path

SUBFOLDERS = ["Answer", "Test"]

# =========================
# PROCESS
# =========================

def render_folder(folder: Path):
    midi_files = sorted(folder.glob("*.mid"))

    for midi_path in midi_files:
        audio_path = midi_path.with_suffix(".wav")

        print(f"Rendering: {midi_path.name}")

        render_midi_to_audio(
            midi_path,
            audio_path,
            SF2_PATH
        )


def main():
    for sub in SUBFOLDERS:
        folder = BASE_DIR / sub

        if not folder.exists():
            print(f"Folder not found: {folder}")
            continue

        print(f"\n=== Processing {sub} ===")
        render_folder(folder)


if __name__ == "__main__":
    main()