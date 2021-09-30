from typing import List, Tuple
from PIL import ImageDraw
import colorsys


def create_palette(n_colors: int) -> List[Tuple[int, ]]:
    hsv_colors = [(x / n_colors, 0.8, 0.8) for x in range(n_colors)]
    rgb_colors = [colorsys.hsv_to_rgb(*hsv_color) for hsv_color in hsv_colors]
    return [tuple(int(value * 255) for value in color) for color in rgb_colors]


def draw_circle(draw: ImageDraw, position: Tuple[int, int], radius: int,
                color: Tuple[int, int, int]):
    draw.ellipse((position[0] - radius,
                  position[1] - radius,
                  position[0] + radius,
                  position[1] + radius), fill=color)
