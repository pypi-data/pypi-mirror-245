#!/usr/bin/env python3
"""peelee is one module to generate random palette and colors.


"""

import colorsys
import getopt
import random
import sys


def fg(hex_color, msg):
    """Decorate msg with hex_color in foreground."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[38;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def bg(hex_color, msg):
    """Decorate msg with hex_color in background."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[48;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def hex2rgb(hex_color):
    """ "Convert."""
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i: i + 2], 16) for i in (0, 2, 4))
    return rgb_color


def hex2hls(hex_color):
    """ "Convert."""
    rgb_color = hex2rgb(hex_color)
    normalized_rgb = (
        rgb_color[0] / 255.0,
        rgb_color[1] / 255.0,
        rgb_color[2] / 255.0,
    )
    hls_color = colorsys.rgb_to_hls(
        normalized_rgb[0], normalized_rgb[1], normalized_rgb[2]
    )
    return hls_color


def hls2hex(hls_color):
    """
    Convert HSL color to HEX code.

    Parameter:
    hls_color - tuple containing hue, lightness, and saturation color codes
    such as (0.5277777777777778, 0.04, 1).
    """
    rgb_color = colorsys.hls_to_rgb(hls_color[0], hls_color[1], hls_color[2])
    scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    return rgb2hex(scaled_rgb)


def rgb2hex(rgb_color):
    """ "Convert."""
    scaled_rgb = rgb_color
    if isinstance(rgb_color[0], float):
        scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    hex_color = f"#{scaled_rgb[0]:02X}{scaled_rgb[1]:02X}{scaled_rgb[2]:02X}"
    return hex_color


def get_scheme_colors(hex_color, n_colors=7):
    """"""
    assert hex_color is not None, "Invalid argument: hex_color is None."
    assert (
        n_colors is not None and isinstance(n_colors, int) and n_colors > 0
    ), f"Invalid argument: n_colors = {n_colors}"
    hls_color = hex2hls(hex_color)
    triadic_colors = []
    for offset in range(0, 360, 360 // n_colors):
        triadic_colors.append(
            ((hls_color[0] + offset / 360) % 1.0, hls_color[1], hls_color[2])
        )
    return [hls2hex(hls_color) for hls_color in triadic_colors][0:n_colors]


def _padding(num, target_length):
    """
    Padding left for number to make it's string format length reaches the target length.

    This is mainly used to construct valid hex color number in R,G,B
    position. Example, if the given num is a hex number 0xf and the
    target length is 2, then the padding result is 0f.
    """
    str_num = str(num)
    if str_num.startswith("0x"):
        str_num = str_num[2:]
    if len(str_num) < target_length:
        str_num = (
            f"{''.join(['0' for i in range(target_length - len(str_num))])}{str_num}"
        )
    return str_num


def lighter(base_color, n_color):
    """Given base color, return 'n' color hex codes from base color to lightest
    color."""
    color_rgb = tuple(int(base_color[1:][i: i + 2], 16) for i in (0, 2, 4))
    color_rgb_ligher = tuple(
        list(range(color, 255, (255 - color) // n_color))[0:n_color]
        for color in color_rgb
    )

    lighter_colors = [
        f"#{''.join(tuple(_padding(hex(color_ligher[index]), 2) for color_ligher in color_rgb_ligher))}"
        for index in range(0, n_color)
    ]

    return lighter_colors


def random_color(
    min_color=0,
    max_color=231,
    base_colors_total=7,
    gradations_total=24,
):
    """
    Generate random color hex codes.

    Firstly, it will generate random integer from min_color (0-(255 - gradations_total - 1)) to max_color (0-(255 - gradations_total)).
    The max_color should be less than (255 - gradations_total) because it needs the room to generate lighter colors.

    To generate darker colors, use smaller value for max_color.
    To generate ligher colors, use bigger value for min_color.

    It's recommended to use default values.
    If you want to make change, please make sure what you are doing.

    Secondly, it will generate 'gradations_total' different hex color codes from base color to the lightest color.
    Note that 'gradations_total' includes base color also. It means it will generate 'gradations_total - 1' lighter colors besides base color.

    Parameters:
        min_color - minimum color code. default: 0.
        max_color - maximum color code. default: 254 (cannot be bigger value).
        base_colors_total - how many base colors to generate. default: 7.
        gradations_total - how many lighter colors to generate. default: 24.

    Retrun:
        Generated random base colors and all lighter colors of each base color.
        The returned value is a two-dimention list. First dimention length is the value of base_colors_total. Second dimention length is gradations_total.
    """
    if gradations_total < 0 or gradations_total > 253:
        gradations_total = 24
    if min_color < 0 or min_color > (255 - gradations_total -1):
        min_color = 0
    if max_color <= min_color or max_color >= (255 - gradations_total):
        max_color = 255 - gradations_total - 1
    
    _min = min_color
    _max = max_color
    
    random_hex_color_code = "#"
    for _ in range(0, 3):
        random_int = random.randint(_min, _max)
        _random_color = _padding(hex(random_int), 2)
        random_hex_color_code = random_hex_color_code + _random_color

    base_colors = get_scheme_colors(random_hex_color_code, base_colors_total)[
        0:base_colors_total
    ]

    random_colors = []
    for base_color in base_colors:
        lighter_colors = lighter(base_color, gradations_total)
        random_colors.append(lighter_colors)

    return random_colors


class Palette:
    """Generate palette colors."""

    def __init__(self, base_colors_total=5, gradations_total=6, general_max_color=200, dark_max_color=30):
        # random colors are used for sections, components, and pieces
        self.base_colors_total = base_colors_total
        self.gradations_total = gradations_total
        self.general_max_color = general_max_color
        self.dark_max_color = dark_max_color

    def generate_palette_colors(self):
        """
        Generate random palette.

        6 group base colors: 5 base colors + dark gray color. echo base
        color has 6 different colors from dark to light. placeholders
        are from light to dark, so need to reverse the order.
        """
        random_colors = random_color(
            max_color=self.general_max_color,
            base_colors_total=self.base_colors_total,
            gradations_total=self.gradations_total,
        )

        # dark colors are generated by default and used as base color in theme
        dark_colors = random_color(
            max_color=self.dark_max_color, base_colors_total=1, gradations_total=self.gradations_total
        )

        random_colors.extend(dark_colors)
        for r_colors in random_colors:
            r_colors.reverse()
        return [color for r_colors in random_colors for color in r_colors]

    def generate_palette(self):
        """
        Generate palette content.

        Palette contains a list of colors. Each color is a pair of color
        name and color code.
        The format is "C_[base color sequence]_[colormap sequence]".

        For example, "C_1_1":"#8f67ff".

        Note:
        The 'base color sequence' starts from 1 to base_colors_total (not
        included)
        The 'colormap sequence' starts from 0 to gradations_total (not
        included)
        When "colormap sequence" is 0, then it represents the lightest color.

        One continuous colormap is for one base color and consists of a
        group of colors from lightest color to the base color.

        Return:
        A list of palette colors.
        """
        palette_color_codes = self.generate_palette_colors()
        base_color_sequence = 0
        colormap_sequence = 0
        palette_colors = []
        for index, color in enumerate(palette_color_codes):
            colormap_sequence = index % self.gradations_total
            if colormap_sequence == 0:
                base_color_sequence += 1
            str_base_color_sequence = _padding(base_color_sequence, len(str(self.base_colors_total)))
            str_colormap_sequence = _padding(colormap_sequence, len(str(self.gradations_total)))
            color_name = f"C_{str_base_color_sequence}_{str_colormap_sequence}"
            palette_colors.append(f"{color_name}:{color}")
        return palette_colors


def generate_palette():
    """Generate palette colors."""
    return Palette().generate_palette()


def main():
    """Test."""
    opts, _ = getopt.getopt(
        sys.argv[1:], "b:g:m:M:", ["--base_colors_total=", "--gradations_total=", "--general_max_color=", "--dark_max_color="]
    )
    base_colors_total = 5
    gradations_total = 6
    general_max_color = 200
    dark_max_color = 30
    for option, value in opts:
        if option in ("-b", "--base_colors_total"):
            base_colors_total = int(value)
        if option in ("-g", "--gradations_total"):
            gradations_total = int(value)
        if option in ("-m", "--general_max_color"):
            general_max_color = int(value)
        if option in ("-M", "--dark_max_color"):
            dark_max_color = int(value)
    palette = Palette(base_colors_total, gradations_total, general_max_color, dark_max_color)
    for _color in palette.generate_palette():
        _hex = _color.split(":")[1]
        print(bg(_hex, _color))


if __name__ == "__main__":
    main()
