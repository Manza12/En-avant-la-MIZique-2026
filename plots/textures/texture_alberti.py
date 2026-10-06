from texture_to_svg import texture_to_svg

T = [
    [2, 0, 0, 0],
    [0, 0, 2, 0],
    [0, 2, 0, 2],
]



texture_to_svg(
    T,
    resolution="Halb",
    resolution_pos=4,
    output_svg="texture_alberti.svg",
    add_rhythms=False,
    color=(39, 54, 86),
    x=0.3, stroke_width=1,
    tick_offset=0.25,
)

