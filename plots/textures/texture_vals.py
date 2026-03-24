from texture_to_svg import texture_to_svg

T = [
    [2, 0, 0],
    [0, 2, 2],
]



texture_to_svg(
    T,
    resolution="Vier",
    resolution_pos=1,
    output_svg="texture_vals.svg",
    add_rhythms=False
)

