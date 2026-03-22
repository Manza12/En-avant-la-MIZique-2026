from texture_to_svg import texture_to_svg

T = [
    [0, 0, 0, 0, 2, 1, 1, 1],
    [0, 2, 2, 2, 0, 0, 0, 0],
]

T_prime = [
    [0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1],
    [0, 2, 2, 2, 0, 0, 0, 0],
]

texture_to_svg(
    T,
    resolution="Halb",
    resolution_pos=4,
    output_svg="texture_beethoven.svg",
)

texture_to_svg(
    T_prime,
    resolution="Halb",
    resolution_pos=4,
    output_svg="texture_beethoven_prime.svg",
)

texture_to_svg(
    T,
    resolution="Halb",
    resolution_pos=4,
    add_rhythms=False,
    output_svg="texture_beethoven_no_R.svg",
)