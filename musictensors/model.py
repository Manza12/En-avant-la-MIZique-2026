import warnings
from fractions import Fraction as frac
from typing import Set, List, Tuple, Union, Optional
from multimethod import multimethod
from .constants import ROMAN_NUMERAL_TO_SHIFT, ROMAN_NUMERAL_TO_FACTORS


# Time
class Hit:
    @multimethod
    def __init__(self, hit: 'Hit'):
        self.onset = hit.onset
        self.duration = hit.duration

    @multimethod
    def __init__(self, onset: frac, duration: frac):
        self.onset = onset
        self.duration = duration

    @multimethod
    def __init__(self, onset: str, duration: str):
        self.onset = frac(onset)
        self.duration = frac(duration)

    @multimethod
    def __init__(self, onset_duration: Tuple[frac, frac]):
        self.onset, self.duration = onset_duration

    def __radd__(self, other: frac) -> 'Hit':
        return Hit(self.onset + other, self.duration)

    def __hash__(self):
        return hash((self.onset, self.duration))

    def __eq__(self, other):
        if not isinstance(other, Hit):
            return False
        return self.onset == other.onset and self.duration == other.duration

    def __repr__(self):
        return f"({self.onset}, {self.duration})"


class Rhythm:
    @multimethod
    def __init__(self):
        self.hits = set()

    @multimethod
    def __init__(self, rhythm: 'Rhythm'):
        self.hits = {h for h in rhythm.hits}

    @multimethod
    def __init__(self, hits: Set[Hit]):
        self.hits = hits

    @multimethod
    def __init__(self, *hits: Hit):
        self.hits = set(hits)

    @multimethod
    def __init__(self, hits: Set[Tuple[frac, frac]]):
        self.hits = {Hit(h) for h in hits}

    @multimethod
    def __init__(self, *hits: Tuple[frac, frac]):
        self.hits = {Hit(h) for h in hits}

    def __add__(self, shift: frac) -> 'Rhythm':
        return Rhythm({shift + Hit(hit.onset, hit.duration) for hit in self.hits})

    def __mul__(self, ratio: Union[int, frac]) -> 'Rhythm':
        return Rhythm({Hit(hit.onset * ratio, hit.duration * ratio) for hit in self.hits})

    def __eq__(self, other):
        if not isinstance(other, Rhythm):
            return False
        return self.hits == other.hits

    def __repr__(self):
        return '{' + f"{', '.join([str(h) for h in self.hits])}" + '}'


class Texture:
    @multimethod
    def __init__(self):
        self.rhythms = []
        self.start = None
        self.end = None

    @multimethod
    def __init__(self, texture: 'Texture'):
        self.rhythms = [r for r in texture.rhythms]
        self.start = texture.start
        self.end = texture.end

    @multimethod
    def __init__(self, *rhythms: Rhythm, start=None, end=None):
        self.rhythms = [r for r in rhythms]
        if start is None:
            start = frac(0)
        if end is None:
            end = self.endpoint
        self.start = start
        self.end = end

    @multimethod
    def __init__(self, rhythms: List[Rhythm], start=None, end=None):
        self.__init__(*rhythms, start=start, end=end)

    @multimethod
    def __matmul__(self, harmony: 'Harmony') -> 'HarmonicTexture':
        return HarmonicTexture(harmony, self)

    @multimethod
    def __matmul__(self, orchestration: 'Orchestration') -> 'OrchestredTexture':
        return OrchestredTexture(orchestration, self)

    @multimethod
    def __matmul__(self, orchestration: 'Section') -> 'OrchestredTexture':
        orchestration = orchestration * len(self)
        return OrchestredTexture(orchestration, self)

    @multimethod
    def __add__(self, other: 'Texture') -> 'Texture':
        return Texture(self.rhythms + other.rhythms,
                       start=min(self.start, other.start),
                       end=max(self.end, other.end))

    @multimethod
    def __add__(self, other: frac) -> 'Texture':
        return Texture([r + other for r in self.rhythms],
                       start=self.start + other, end=self.end + other)

    @multimethod
    def __mul__(self, other: 'Texture') -> 'Texture':
        return Texture(self.rhythms + [r + self.end for r in other.rhythms],
                       start=self.start,
                       end=self.end + other.end - other.start)

    @multimethod
    def __mul__(self, ratio: frac) -> 'Texture':
        return Texture([r * ratio for r in self.rhythms],
                       start=self.start * ratio,
                       end=self.end * ratio)

    @multimethod
    def __mul__(self, other: int) -> 'Texture':
        assert isinstance(other, int) and other > 0, "The other must be a positive integer."
        result = self
        for _ in range(other - 1):
            result = result + self
        return result

    def __pow__(self, other: int) -> 'Texture':
        assert isinstance(other, int) and other > 0, "The exponent must be a positive integer."
        result = self
        for _ in range(other - 1):
            result = result * self
        return result

    def __eq__(self, other):
        if not isinstance(other, Texture):
            return False
        return self.rhythms == other.rhythms

    def __len__(self):
        return len(self.rhythms)

    def __repr__(self):
        return f"[{', '.join([str(r) for r in self.rhythms])}]"

    def __getitem__(self, key):
        return Texture(self.rhythms[key], start=self.start, end=self.end)

    @property
    def endpoint(self) -> frac:
        result = frac(0)
        for rhythm in self.rhythms:
            for hit in rhythm.hits:
                end = hit.onset + hit.duration
                if end > result:
                    result = end
        return result

    @property
    def duration(self) -> frac:
        return self.end - self.start


# Frequency
class Pitch:
    @multimethod
    def __init__(self, pitch: 'Pitch'):
        self.number = pitch.number

    @multimethod
    def __init__(self, number: int):
        self.number = number

    @multimethod
    def __add__(self, other: 'Pitch') -> 'Pitch':
        return Pitch(self.number + other.number)

    @multimethod
    def __add__(self, other: int) -> 'Pitch':
        return Pitch(self.number + other)

    @multimethod
    def __sub__(self, other: 'Pitch') -> 'Pitch':
        return Pitch(self.number - other.number)

    @multimethod
    def __sub__(self, other: int) -> 'Pitch':
        return Pitch(self.number - other)

    @multimethod
    def __add__(self, other: 'Chord') -> 'Chord':
        if len(other.pitches) == 0:
            return Chord()
        return Chord({self + p for p in other.pitches}, velocity=other.velocity)

    @multimethod
    def __add__(self, other: 'Harmony') -> 'Harmony':
        return Harmony([self + c for c in other.chords])

    @multimethod
    def __add__(self, other: 'ScoreTensor') -> 'ScoreTensor':
        return ScoreTensor(self + other.harmony,
                           other.texture,
                           other.orchestration)

    @multimethod
    def __add__(self, other: 'HarmonicTexture') -> 'HarmonicTexture':
        return HarmonicTexture(self + other.harmony, other.texture)

    def __lt__(self, other):
        return self.number < other.number

    def __eq__(self, other):
        if not isinstance(other, Pitch):
            return False
        return self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def __repr__(self):
        return str(self.number)


class Chord:
    default_velocity = 90

    @multimethod
    def __init__(self, velocity: int = None):
        self.pitches = set()
        self.velocity = velocity if velocity is not None else self.default_velocity

    @multimethod
    def __init__(self, chord: 'Chord'):
        self.pitches = {p for p in chord.pitches}
        self.velocity = chord.velocity

    @multimethod
    def __init__(self, pitches: Set[Pitch], velocity: int = None):
        self.pitches = pitches
        self.velocity = velocity if velocity is not None else self.default_velocity

    @multimethod
    def __init__(self, *pitches: Pitch, velocity: int = None):
        self.pitches = set(pitches)
        self.velocity = velocity if velocity is not None else self.default_velocity

    @multimethod
    def __init__(self, pitches: Set[int], velocity: int = None):
        self.pitches = {Pitch(p) for p in pitches}
        self.velocity = velocity if velocity is not None else self.default_velocity

    def __add__(self, other: int) -> 'Chord':
        return Chord({p + other for p in self.pitches}, velocity=self.velocity)

    def __sub__(self, other: int) -> 'Chord':
        return Chord({p - other for p in self.pitches}, velocity=self.velocity)

    def __or__(self, other: 'Chord') -> 'Chord':
        return Chord(self.pitches | other.pitches, velocity=max(self.velocity, other.velocity))

    def __getitem__(self, key):
        ordered_pitches = sorted(list(self.pitches))
        return Chord({ordered_pitches[i] for i in key}, velocity=self.velocity)

    def __eq__(self, other):
        if not isinstance(other, Chord):
            return False
        return self.pitches == other.pitches

    def __repr__(self):
        return '{' + f"{', '.join([str(p) for p in self.pitches])}" + '}'

    @classmethod
    def from_roman_numeral(cls, roman_numeral: str,
                           inversion: int = 0,
                           octave: int = 0,
                           n_notes: Optional[int] = None
                           ) -> 'Chord':
        try:
            shifts = ROMAN_NUMERAL_TO_SHIFT[roman_numeral]
        except KeyError:
            raise ValueError(f"Roman numeral: {roman_numeral} not found.")

        n = len(shifts)
        shifts_spacing = [(shifts[(i + 1) % n] - shifts[i % n]) % 12 for i in range(len(shifts))]
        if n_notes is None:
            n_notes = n

        if inversion != 0:
            shifts = shifts[inversion:] + shifts[:inversion]
            shifts_spacing = shifts_spacing[inversion:] + shifts_spacing[:inversion]

        bass = shifts[0] + 12 * octave
        return cls({bass + sum(shifts_spacing[:i]) for i in range(n_notes)})


class Harmony:
    @multimethod
    def __init__(self):
        self.chords = []

    @multimethod
    def __init__(self, harmony: 'Harmony'):
        self.chords = [c for c in harmony.chords]

    @multimethod
    def __init__(self, chords: List[Chord], velocity: int = None):
        self.chords = chords
        if velocity is not None:
            for c in self.chords:
                c.velocity = velocity

    @multimethod
    def __init__(self, *chords: Chord, velocity: int = None):
        self.__init__(list(chords), velocity=velocity)

    @multimethod
    def __init__(self, chords: List[Set[int]], velocity: int = Chord.default_velocity):
        self.chords = [Chord(c, velocity=velocity) for c in chords]

    # @multimethod
    # def __init__(self, *chords: Union[Chord, Set[Pitch], Set[int]], velocity: int = Chord.default_velocity):
    #     self.chords = [Chord(c) for c in chords]

    @multimethod
    def __add__(self, other: 'Harmony') -> 'Harmony':
        return Harmony(self.chords + other.chords)

    @multimethod
    def __add__(self, other: int) -> 'Harmony':
        return Harmony(*[c + other for c in self.chords])

    def __sub__(self, other: int) -> 'Harmony':
        assert type(other) == int, "The parameter 'other' must be an integer."
        return Harmony(*[c - other for c in self.chords])

    @multimethod
    def __matmul__(self, texture: Texture) -> 'HarmonicTexture':
        return HarmonicTexture(self, texture)

    @multimethod
    def __matmul__(self, orchestration: 'Orchestration') -> 'HarmonicOrchestration':
        return HarmonicOrchestration(self, orchestration)

    def __mul__(self, other: int):
        assert isinstance(other, int) and other > 0, "The parameter 'other' must be a positive integer."
        result = self
        for _ in range(other - 1):
            result = result + self
        return result

    def __or__(self, other: 'Harmony') -> 'Harmony':
        return Harmony(*(c_self | c_other for c_self, c_other in zip(self.chords, other.chords)))

    def __eq__(self, other):
        if not isinstance(other, Harmony):
            return False
        return self.chords == other.chords

    def __getitem__(self, key):
        return Harmony(self.chords[key])

    def __len__(self):
        return len(self.chords)

    def __repr__(self):
        return f"[{', '.join([str(c) for c in self.chords])}]"

    @classmethod
    def from_chord(cls, chord: Chord):
        ordered_pitches = sorted(chord.pitches, key=lambda p: p.number)
        return Harmony([Chord(c, velocity=chord.velocity) for c in ordered_pitches])

    @classmethod
    def from_roman_numeral(cls, roman_numeral: str, factors: List[str], octave: int = 0, velocity: int = Chord.default_velocity):
        roman_numeral_dict = ROMAN_NUMERAL_TO_FACTORS[roman_numeral]
        shifts = list(roman_numeral_dict.values())
        keys = list(roman_numeral_dict.keys())
        root = roman_numeral_dict['1']
        n = len(shifts)
        shifts_spacing = [(shifts[(i + 1) % n] - shifts[i % n]) % 12 for i in range(len(shifts))]
        chords = []
        cum_shift = 0
        i = 0
        for f, factor in enumerate(factors):
            while factor != keys[i] and factor != '-':
                cum_shift += shifts_spacing[i]
                i = (i + 1) % n

            chord = Chord(Pitch(root + cum_shift + 12 * octave), velocity=velocity)
            chords.append(chord)

            if f < len(factors) - 1 and factors[f + 1] == '-':
                pass
            else:
                cum_shift += shifts_spacing[i]
                i = (i + 1) % n

        return Harmony(chords)

    def extend(self, n: int = 1):
        return self + Harmony([Chord() for _ in range(n)])

    def permute(self, permutation: List[int]):
        assert len(permutation) == len(self)
        return Harmony([self.chords[i] for i in permutation])

    def flat(self) -> 'Harmony':
        flatten_chord = Chord()
        for chord in self.chords:
            flatten_chord = flatten_chord | chord
        return Harmony([flatten_chord])

    def __reversed__(self):
        return Harmony(list(reversed(self.chords)))


# Instruments
class Instrument:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Instrument):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class Section:
    @multimethod
    def __init__(self):
        self.instruments = set()

    @multimethod
    def __init__(self, section: 'Section'):
        self.instruments = {i for i in section.instruments}

    @multimethod
    def __init__(self, instruments: Set[Instrument]):
        self.instruments = instruments

    @multimethod
    def __init__(self, *instruments: Instrument):
        self.instruments = set(instruments)

    def __mul__(self, other: int):
        return Orchestration(*[self for _ in range(other)])

    def __eq__(self, other):
        if not isinstance(other, Section):
            return False
        return self.instruments == other.instruments

    def __repr__(self):
        return '{' + f"{', '.join([str(i) for i in self.instruments])}" + '}'

    def __hash__(self):
        return hash(tuple(sorted(self.instruments, key=lambda i: i.name)))


class Orchestration:
    @multimethod
    def __init__(self):
        self.sections = []

    @multimethod
    def __init__(self, orchestration: 'Orchestration'):
        self.sections = [s for s in orchestration.sections]

    @multimethod
    def __init__(self, sections: List[Section]):
        self.sections = sections

    @multimethod
    def __init__(self, *sections: Section):
        if len(sections) == 1 and isinstance(sections[0], list):
            self.sections = []
        else:
            self.sections = list(sections)

    def __getitem__(self, key):
        return Orchestration(self.sections[key])

    def __len__(self):
        return len(self.sections)

    def __add__(self, other: 'Orchestration') -> 'Orchestration':
        return Orchestration(self.sections + other.sections)

    def __mul__(self, other: int) -> 'Orchestration':
        assert isinstance(other, int) and other > 0, "The parameter 'other' must be a positive integer."
        result = self
        for _ in range(other - 1):
            result = result + self
        return result

    @multimethod
    def __matmul__(self, harmony: Harmony) -> 'HarmonicOrchestration':
        return HarmonicOrchestration(harmony, self)

    @multimethod
    def __matmul__(self, texture: Texture) -> 'OrchestredTexture':
        return OrchestredTexture(self, texture)

    def __eq__(self, other):
        if not isinstance(other, Orchestration):
            return False
        return self.sections == other.sections

    def __repr__(self):
        return f"[{', '.join([str(g) for g in self.sections])}]"


# Time-Frequency
class Note:
    def __init__(self, pitch: Pitch, onset: frac, duration: frac, instrument: Instrument, velocity: int):
        self.pitch = pitch
        self.onset = onset
        self.duration = duration
        self.instrument = instrument
        self.velocity = velocity

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        same_pitch = self.pitch == other.pitch
        same_onset = self.onset == other.onset
        same_duration = self.duration == other.duration
        same_instrument = self.instrument == other.instrument
        return same_pitch and same_onset and same_duration and same_instrument

    def __hash__(self):
        return hash((self.pitch, self.onset, self.duration, self.instrument))

    def __repr__(self):
        return f"({self.pitch}, {self.onset}, {self.duration}, {self.instrument})"

    @property
    def start(self):
        return self.onset

    @property
    def end(self):
        return self.onset + self.duration

    @property
    def frequency(self):
        return self.pitch.number


class HarmonicTexture:
    @multimethod
    def __init__(self):
        self.harmony = Harmony()
        self.texture = Texture()

    @multimethod
    def __init__(self, harmonic_texture: 'HarmonicTexture'):
        self.harmony = Harmony(harmonic_texture.harmony)
        self.texture = Texture(harmonic_texture.texture)

    @multimethod
    def __init__(self, harmony: Harmony, texture: Texture):
        same_length = len(harmony) == len(texture)
        if not same_length:
            warnings.warn("Harmony and texture have different lengths; " +
                          f"Harmony: {len(harmony)}, " +
                          f"Texture: {len(texture)}. " +
                          f"Clipping to the minimum length ({min(len(harmony), len(texture))}).",
                          stacklevel=5)

        min_length = min(len(harmony), len(texture))

        self.harmony = harmony[:min_length]
        self.texture = texture[:min_length]

    def __add__(self, other: 'HarmonicTexture') -> 'HarmonicTexture':
        return HarmonicTexture(self.harmony + other.harmony, self.texture + other.texture)

    def __mul__(self, other: 'HarmonicTexture') -> 'HarmonicTexture':
        return HarmonicTexture(self.harmony + other.harmony, self.texture * other.texture)

    def __pow__(self, power: int) -> 'HarmonicTexture':
        return HarmonicTexture(self.harmony * power, self.texture ** power)

    @multimethod
    def __matmul__(self, other: Orchestration) -> 'ScoreTensor':
        return ScoreTensor(self.harmony, self.texture, other)

    @multimethod
    def __matmul__(self, other: Section) -> 'ScoreTensor':
        orchestration = other * len(self)
        return ScoreTensor(self.harmony, self.texture, orchestration)

    @multimethod
    def __matmul__(self, other: Instrument) -> 'ScoreTensor':
        section = Section(other)
        return self @ section

    def __len__(self):
        assert len(self.texture) == len(self.harmony)
        return len(self.texture)

    def __eq__(self, other):
        if not isinstance(other, HarmonicTexture):
            return False
        return self.harmony == other.harmony and self.texture == other.texture

    def notes(self, instrument_name: str = 'Acoustic Grand Piano'):
        result = set()

        instrument = Instrument(instrument_name)

        for rhythm, chord in zip(self.texture.rhythms, self.harmony.chords):
            for hit in rhythm.hits:
                for pitch in chord.pitches:
                    result.add(Note(pitch, hit.onset, hit.duration, instrument, chord.velocity))
        return result

    def ordered_notes(self, instrument_name: str = 'Acoustic Grand Piano'):
        notes = self.notes(instrument_name)
        return sorted(notes, key=lambda note: (note.onset, note.pitch.number))

    def to_midi(self, bpm=100):
        from .midi import to_midi
        return to_midi(self.notes(), bpm)


class HarmonicOrchestration:
    @multimethod
    def __init__(self):
        self.harmony = Harmony()
        self.orchestration = Orchestration()

    @multimethod
    def __init__(self, harmonic_orchestration: 'HarmonicOrchestration'):
        self.harmony = Harmony(harmonic_orchestration.harmony)
        self.orchestration = Orchestration(harmonic_orchestration.orchestration)

    @multimethod
    def __init__(self, harmony: Harmony, orchestration: Orchestration):
        same_length = len(harmony) == len(orchestration)
        if not same_length:
            warnings.warn("Harmony and orchestration have different lengths; "
                          f"Harmony: {len(harmony)}, "
                          f"Instrumentation: {len(orchestration)}")

        self.harmony = harmony
        self.orchestration = orchestration

    def __add__(self, other: 'HarmonicOrchestration') -> 'HarmonicOrchestration':
        return HarmonicOrchestration(self.harmony + other.harmony, self.orchestration + other.orchestration)

    def __eq__(self, other):
        if not isinstance(other, HarmonicOrchestration):
            return False
        return self.harmony == other.harmony and self.orchestration == other.orchestration


class OrchestredTexture:
    @multimethod
    def __init__(self):
        self.orchestration = Orchestration()
        self.texture = Texture()

    @multimethod
    def __init__(self, texture_orchestration: 'OrchestredTexture'):
        self.orchestration = Orchestration(texture_orchestration.orchestration)
        self.texture = Texture(texture_orchestration.texture)

    @multimethod
    def __init__(self, orchestration: Orchestration, texture: Texture):
        same_length = len(texture) == len(orchestration)
        if not same_length:
            warnings.warn("Texture and orchestration have different lengths; "
                          f"Texture: {len(texture)}, "
                          f"Instrumentation: {len(orchestration)}")

        self.orchestration = orchestration
        self.texture = texture

    def __add__(self, other: 'OrchestredTexture') -> 'OrchestredTexture':
        return OrchestredTexture(self.orchestration + other.orchestration, self.texture + other.texture)

    def __mul__(self, other: 'OrchestredTexture') -> 'OrchestredTexture':
        return OrchestredTexture(self.orchestration + other.orchestration, self.texture * other.texture)

    def __pow__(self, power: int) -> 'OrchestredTexture':
        return OrchestredTexture(self.orchestration * power, self.texture ** power)

    def __eq__(self, other):
        if not isinstance(other, OrchestredTexture):
            return False
        return self.texture == other.texture and self.orchestration == other.orchestration

    def __matmul__(self, other: Harmony) -> 'ScoreTensor':
        return ScoreTensor(other, self.texture, self.orchestration)


class ScoreTensor:
    @multimethod
    def __init__(self):
        self.harmony = Harmony()
        self.texture = Texture()
        self.orchestration = Orchestration()

    @multimethod
    def __init__(self, score_tensor: 'ScoreTensor'):
        self.harmony = Harmony(score_tensor.harmony)
        self.texture = Texture(score_tensor.texture)
        self.orchestration = Orchestration(score_tensor.orchestration)

    @multimethod
    def __init__(self, harmony: Harmony, texture: Texture, orchestration: Orchestration):
        same_length = len(harmony) == len(texture) == len(orchestration)
        if not same_length:
            warnings.warn("Harmony, texture and orchestration have different lengths; "
                          f"Harmony: {len(harmony)}, "
                          f"Texture: {len(texture)}, "
                          f"Instrumentation: {len(orchestration)}")
        min_length = min(len(harmony), len(texture), len(orchestration))
        self.texture = texture[:min_length]
        self.harmony = harmony[:min_length]
        self.orchestration = orchestration[:min_length]

    def __mul__(self, other: 'ScoreTensor') -> 'ScoreTensor':
        new_harmony = self.harmony + other.harmony if self.harmony is not None else other.harmony
        new_texture = self.texture * other.texture if self.texture is not None else other.texture
        new_orchestration = self.orchestration + other.orchestration \
            if self.orchestration is not None else other.orchestration
        return ScoreTensor(new_harmony, new_texture, new_orchestration)

    @multimethod
    def __add__(self, other: 'ScoreTensor') -> 'ScoreTensor':
        new_harmony = self.harmony + other.harmony if self.harmony is not None else other.harmony
        new_texture = self.texture + other.texture if self.texture is not None else other.texture
        new_orchestration = self.orchestration + other.orchestration \
            if self.orchestration is not None else other.orchestration
        return ScoreTensor(new_harmony, new_texture, new_orchestration)

    @multimethod
    def __add__(self, other: frac):
        new_texture = self.texture + other if self.texture is not None else None
        return ScoreTensor(self.harmony, new_texture, self.orchestration)

    @multimethod
    def __add__(self, other: int):
        new_harmony = self.harmony + other if self.harmony is not None else None
        return ScoreTensor(new_harmony, self.texture, self.orchestration)

    def __pow__(self, other: int) -> 'ScoreTensor':
        assert isinstance(other, int) and other > 0, "The exponent must be a positive integer."
        result = self
        for _ in range(other - 1):
            result = result * self
        return result

    def __eq__(self, other):
        if not isinstance(other, ScoreTensor):
            return False
        same_texture = self.texture == other.texture
        same_harmony = self.harmony == other.harmony
        same_orchestration = self.orchestration == other.orchestration
        return same_texture and same_harmony and same_orchestration

    @property
    def start(self):
        return self.texture.start

    @start.setter
    def start(self, value):
        self.texture.start = value

    @property
    def end(self):
        return self.texture.end

    @end.setter
    def end(self, value):
        self.texture.end = value

    def notes(self) -> Set['Note']:
        result = set()

        for rhythm, chord, group in zip(self.texture.rhythms, self.harmony.chords, self.orchestration.sections):
            for hit in rhythm.hits:
                for pitch in chord.pitches:
                    for instrument in group.instruments:
                        result.add(Note(pitch, hit.onset, hit.duration, instrument, chord.velocity))
        return result

    def ordered_notes(self) -> List['Note']:
        notes = self.notes()
        return sorted(notes, key=lambda note: (note.onset, note.pitch.number))

    def to_midi(self, bpm=100):
        from .midi import to_midi
        return to_midi(self.notes(), bpm)
