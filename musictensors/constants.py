from typing import Dict, List


ROMAN_NUMERAL_TO_FACTORS: Dict[str, Dict[str, int]] = {
    'I': {'1': 0, '3': 4, '5': 7},
    'i': {'1': 0, '3': 3, '5': 7},
    'iio7': {'1': 2, '3': 5, '5': 8, '7': 0},
    'N': {'1': 1, '3': 5, '5': 8},
    'iv': {'1': 5, '3': 8, '5': 0},
    'IV': {'1': 5, '3': 9, '5': 0},
    'V7': {'1': 7, '3': 11, '5': 2, '7': 5},
    'V': {'1': 7, '3': 11, '5': 2},
}


ROMAN_NUMERAL_TO_SHIFT: Dict[str, List[int]] = {
    k: list(ROMAN_NUMERAL_TO_FACTORS[k].values()) for k in ROMAN_NUMERAL_TO_FACTORS.keys()
}


INSTRUMENT_MAP = ['Acoustic Grand Piano', 'Bright Acoustic Piano',
                  'Electric Grand Piano', 'Honky-tonk Piano',
                  'Electric Piano 1', 'Electric Piano 2', 'Harpsichord',
                  'Clavinet', 'Celesta', 'Glockenspiel', 'Music Box',
                  'Vibraphone', 'Marimba', 'Xylophone', 'Tubular Bells',
                  'Dulcimer', 'Drawbar Organ', 'Percussive Organ',
                  'Rock Organ', 'Church Organ', 'Reed Organ', 'Accordion',
                  'Harmonica', 'Tango Accordion', 'Acoustic Guitar (nylon)',
                  'Acoustic Guitar (steel)', 'Electric Guitar (jazz)',
                  'Electric Guitar (clean)', 'Electric Guitar (muted)',
                  'Overdriven Guitar', 'Distortion Guitar',
                  'Guitar Harmonics', 'Acoustic Bass',
                  'Electric Bass (finger)', 'Electric Bass (pick)',
                  'Fretless Bass', 'Slap Bass 1', 'Slap Bass 2',
                  'Synth Bass 1', 'Synth Bass 2', 'Violin', 'Viola', 'Cello',
                  'Contrabass', 'Tremolo Strings', 'Pizzicato Strings',
                  'Orchestral Harp', 'Timpani', 'String Ensemble 1',
                  'String Ensemble 2', 'Synth Strings 1', 'Synth Strings 2',
                  'Choir Aahs', 'Voice Oohs', 'Synth Choir', 'Orchestra Hit',
                  'Trumpet', 'Trombone', 'Tuba', 'Muted Trumpet',
                  'French Horn', 'Brass Section', 'Synth Brass 1',
                  'Synth Brass 2', 'Soprano Sax', 'Alto Sax', 'Tenor Sax',
                  'Baritone Sax', 'Oboe', 'English Horn', 'Bassoon',
                  'Clarinet', 'Piccolo', 'Flute', 'Recorder', 'Pan Flute',
                  'Blown bottle', 'Shakuhachi', 'Whistle', 'Ocarina',
                  'Lead 1 (square)', 'Lead 2 (sawtooth)',
                  'Lead 3 (calliope)', 'Lead 4 chiff', 'Lead 5 (charang)',
                  'Lead 6 (voice)', 'Lead 7 (fifths)',
                  'Lead 8 (bass + lead)', 'Pad 1 (new age)', 'Pad 2 (warm)',
                  'Pad 3 (polysynth)', 'Pad 4 (choir)', 'Pad 5 (bowed)',
                  'Pad 6 (metallic)', 'Pad 7 (halo)', 'Pad 8 (sweep)',
                  'FX 1 (rain)', 'FX 2 (soundtrack)', 'FX 3 (crystal)',
                  'FX 4 (atmosphere)', 'FX 5 (brightness)', 'FX 6 (goblins)',
                  'FX 7 (echoes)', 'FX 8 (sci-fi)', 'Sitar', 'Banjo',
                  'Shamisen', 'Koto', 'Kalimba', 'Bagpipe', 'Fiddle',
                  'Shanai', 'Tinkle Bell', 'Agogo', 'Steel Drums',
                  'Woodblock', 'Taiko Drum', 'Melodic Tom', 'Synth Drum',
                  'Reverse Cymbal', 'Guitar Fret Noise', 'Breath Noise',
                  'Seashore', 'Bird Tweet', 'Telephone Ring', 'Helicopter',
                  'Applause', 'Gunshot']
