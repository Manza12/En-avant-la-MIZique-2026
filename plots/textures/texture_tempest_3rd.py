from texture_to_svg import texture_to_svg

T_1 = [
    [2, 0, 0, 0, 0, 0],
    [0, 2, 1, 1, 1, 1],
    [0, 0, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 0],
]

T_2 = [
    [2, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 1, 0],
    [0, 0, 2, 0, 0, 0],
    [0, 2, 0, 0, 0, 0],
]



texture_to_svg(
    T_1,
    resolution="Halb\\Pu",
    resolution_pos=6,
    output_svg="texture_tempest_3rd-1.svg",
    add_rhythms=False,
    color=(39, 54, 86),
    x=0.3, stroke_width=1,
    tick_offset=0.4,
)

texture_to_svg(
    T_2,
    resolution="Halb\\Pu",
    resolution_pos=6,
    output_svg="texture_tempest_3rd-2.svg",
    add_rhythms=False,
    color=(39, 54, 86),
    x=0.3, stroke_width=1,
    tick_offset=0.4,
)

