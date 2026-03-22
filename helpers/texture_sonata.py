from helpers.texture_to_svg import texture_to_svg

T_al = [
    [2, 0, 0, 0],
    [0, 0, 2, 0],
    [0, 2, 0, 2],
]

T_al_reggaeton = [
    [2, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 1, 0, 0],
    [0, 0, 0, 2, 0, 0, 2, 1],
]

T_head = [
    [2, 1, 0, 0],
    [0, 0, 2, 0],
    [0, 0, 0, 2],
]

T_tail_1 = [
    [2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 2, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
]

T_tail_2 = [
    [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 2, 1, 1, 1, 0, 0, 0, 0],
]

texture_to_svg(
    T_al,
    resolution="Halb",
    resolution_pos=4,
    add_rhythms=False,
    output_svg="texture_alberti.svg",
)

texture_to_svg(
    T_al_reggaeton,
    resolution="Halb",
    resolution_pos=8,
    add_rhythms=False,
    output_svg="texture_alberti_reggaeton.svg",
)

texture_to_svg(
    T_head,
    resolution="Halb",
    resolution_pos=2,
    add_rhythms=False,
    output_svg="texture_head.svg",
)

texture_to_svg(
    T_tail_1,
    resolution="Vier",
    resolution_pos=4,
    add_rhythms=False,
    output_svg="texture_tail_1.svg",
)

texture_to_svg(
    T_tail_2,
    resolution="Vier",
    resolution_pos=4,
    add_rhythms=False,
    output_svg="texture_tail_2.svg",
)