import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from .model import ScoreTensor
from .utils import midi_number_to_pitch


def plot_notes(tensor_contraction: ScoreTensor,
               figsize=(10, 5),
               linewidth: float = 5,
               eps: float = 0.01,
               show=False,
               x_tick_start=None,
               x_tick_end=None,
               x_tick_step=None,
               y_tick_step=None,
               color_by_instrument: bool = False,
               ):
    notes = tensor_contraction.notes()
    notes = sorted(notes, key=lambda n: (n.instrument.name, n.start, n.frequency))

    # Build colour map on-the-fly
    if color_by_instrument:
        instruments = sorted({note.instrument.name for note in notes})
        cmap = plt.colormaps['tab20'].resampled(max(len(instruments), 2))
        color_map = {name: cmap(i) for i, name in enumerate(instruments)}
        hit_color = 'black'
    else:
        color_map = {}
        instruments = []
        hit_color = 'red'

    def note_color(note):
        return color_map[note.instrument.name] if color_by_instrument else 'black'

    fig = plt.figure(figsize=figsize)
    for note in notes:
        plt.hlines(note.frequency, float(note.start), float(note.end),
                   color=note_color(note), linewidth=linewidth)

    for note in notes:
        plt.hlines(note.frequency, float(note.start - eps), float(note.start + eps),
                   color=hit_color, linewidth=2 * linewidth)

    if color_by_instrument:
        plt.legend(handles=[mpatches.Patch(color=color_map[n], label=n) for n in instruments],
                   loc='upper left', bbox_to_anchor=(1.01, 1),
                   borderaxespad=0, fontsize='small')
        plt.tight_layout(rect=[0, 0, 1, 1])  # deja un 15% a la derecha para la leyenda

    # Set y-axis
    min_freq = min(note.frequency for note in notes)
    max_freq = max(note.frequency for note in notes)
    ambitus = max_freq - min_freq
    plt.ylim(min_freq - 1, max_freq + 1)
    if y_tick_step is None:
        y_tick_step = ambitus // 5 if ambitus >= 5 else 1
    plt.yticks(range(min_freq, max_freq + 1, y_tick_step))

    # Set y-axis labels
    formatter = plt.FuncFormatter(lambda x, _: f'{midi_number_to_pitch(x)}')
    plt.gca().yaxis.set_major_formatter(formatter)

    # Set x-axis
    if x_tick_start is None:
        x_tick_start = min(note.start for note in notes)
    if x_tick_end is None:
        x_tick_end = max(note.end for note in notes)
    if x_tick_step is None:
        x_tick_step = (x_tick_end - x_tick_start) / 10
    n_x_ticks = int((x_tick_end - x_tick_start) / x_tick_step)
    plt.xticks([float(x_tick_start + x_tick_step * i) for i in range(n_x_ticks + 1)],
               [str(x_tick_start + x_tick_step * i) for i in range(n_x_ticks + 1)])

    if show:
        plt.show()

    return fig