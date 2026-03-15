import matplotlib.pyplot as plt

from .model import TensorContraction
from .utils import midi_number_to_pitch


def plot_notes(tensor_contraction: TensorContraction,
               figsize=(10, 5),
               linewidth: float = 5,
               eps: float = 0.01,
               show=False,
               x_tick_start=None,
               x_tick_end=None,
               x_tick_step=None,
               ):
    notes = tensor_contraction.notes()

    fig = plt.figure(figsize=figsize)
    for note in notes:
        plt.hlines(note.frequency, float(note.start), float(note.end), color='black', linewidth=linewidth)

    for note in notes:
        plt.hlines(note.frequency, float(note.start - eps), float(note.start + eps), color='red', linewidth=2*linewidth)
        # plt.vlines(float(note.start), note.frequency - eps, note.frequency + eps, color='red', linewidth=linewidth)

    # Set y-axis
    min_freq = min(note.frequency for note in notes)
    max_freq = max(note.frequency for note in notes)
    ambitus = max_freq - min_freq
    plt.ylim(min_freq - 1, max_freq + 1)
    plt.yticks(range(min_freq, max_freq + 1, ambitus // 5))

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
    plt.xticks([float(x_tick_start + x_tick_step * i) for i in range(n_x_ticks)],
               [str(x_tick_start + x_tick_step * i) for i in range(n_x_ticks)])

    if show:
        plt.show()

    return fig
