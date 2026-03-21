from helpers.texture_to_svg import texture_to_svg

T = [
    [0, 0, 0, 0, 2, 1, 1, 1],
    [0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 1, 1, 1],
    [0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 1, 1, 1],
    [0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 1, 1, 1],
    [0, 2, 2, 2, 0, 0, 0, 0],
]

texture_to_svg(
    T,
    resolution="Halb",
    resolution_pos=4,
    output_svg="texture_beethoven_orchestra.svg",
    # add_rhythms=False,
)
