def midi_number_to_pitch(number: int) -> str:
    number = int(number + 0.5)
    chroma = number % 12
    octave = number // 12 - 1
    chroma_str = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'][chroma]
    return f'{chroma_str}{octave}'