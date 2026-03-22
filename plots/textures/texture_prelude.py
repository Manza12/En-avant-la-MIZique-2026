from texture_to_svg import texture_to_svg

T = [
    [2, 1, 1, 1, 1, 1, 1, 1],
    [0, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 2, 0, 0, 2, 0, 0],
    [0, 0, 0, 2, 0, 0, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 2],
]

T_1 = [
    [2, 1, 1, 1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 1, 1, 1],
]


texture_to_svg(
    T,
    resolution="Halb",
    resolution_pos=8,
    output_svg="texture_prelude.svg",
    add_rhythms=False
)

texture_to_svg(
    T_1,
    resolution="Halb",
    resolution_pos=8,
    output_svg="texture_prelude_1.svg",
    add_rhythms=False
)
