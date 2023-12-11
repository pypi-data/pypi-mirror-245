from __future__ import annotations
from re import compile as regex_compile
from typing import overload, ClassVar

from .ansi import RESET, FG_COLOR
from .types import *


__all__ = ['Color', 'Fade', 'Col']


def rmansi(text: AnyStringT) -> AnyStringT:
    """
    Remove all the ANSI sequences in a text.

    ### arguments
     - `text`: The text from which ANSI sequences will be removed.

    ### returns
        The text with ANSI sequences removed.
    """
    regexp = regex_compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return regexp.sub('', text)



class Color:
    rgb: tuple[int, int, int]
    """The RGB value of the color"""

    __slots__ = ('rgb',)

    def __init__(self,
                 r: int,
                 g: int,
                 b: int) -> None:
        """
        Create a color using RGB values.

        ### arguments
         - `r `: The red component of the RGB color.
         - `g `: The green component of the RGB color.
         - `b `: The blue component of the RGB color.
        """
        self.rgb = (r, g, b)


    def __repr__(self) -> str:
        return 'color({}, {}, {})'.format(*self.rgb)


    def __or__(self, color: Color) -> Color:
        return self.mix(color)


    @overload
    def __add__(self, other: Color) -> Fade:
        ...


    @overload
    def __add__(self, other: AnyStringT) -> AnyStringT:
        ...


    def __add__(self, other: AnyStringT | Color) -> AnyStringT | Fade:
        if isinstance(other, str):
            return self.colorate(other) + RESET

        elif isinstance(other, Color):
            return Fade([self, other])


    @property
    def hex(self) -> str:
        """The hexadecimal value of the color."""
        return bytes(self.rgb).hex()


    @property
    def ansi(self) -> str:
        return FG_COLOR.format(*map(str, self.rgb))


    @staticmethod
    def fromhex(hex: str) -> Color:
        """
        Create a color from it hexadecimal value.

        ### arguments
         - `hex`: The hexadecimal value of the color.

        ### returns
            The color.
        """
        if hex.startswith('#'):
            hex = hex[1:]
        return Color(*bytes.fromhex(hex))


    def mix(self, color: Color, scale: int = 50) -> Color:
        """
        Mix two colors together.

        ### arguments
         - `color`: The color to mix with the current one.
         -  `scale`: The mixing scale, affecting the ratio of the two colors.

        ### returns
            The new mixed color.
        """
        r = int(self.rgb[0] + (color.rgb[0] - self.rgb[0]) * scale / 100)
        g = int(self.rgb[1] + (color.rgb[1] - self.rgb[1]) * scale / 100)
        b = int(self.rgb[2] + (color.rgb[2] - self.rgb[2]) * scale / 100)
        return Color(r, g, b)


    def colorate(self, text: str) -> str:
        """
        Apply the color to a text.

        ### arguments
         - `text`: The text to which the color will be applied.

        ### returns
            The colored text.
        """
        return self.ansi + text



class Fade:
    colors: list[Color]
    """List of base colors used in the fade effect"""
    collength: int
    """The number of color transitions between each pair of base colors"""
    direction: FadeDirection
    """The direction of the fade when it is over a text"""

    __slots__ = ('colors', 'collength', 'direction')

    def __init__(self,
                 colors: list[Color],
                 collength: int = 10,
                 direction: FadeDirection = 'horizontal') -> None:
        """
        Initialize a Fade with specified colors.

        ### arguments
         - `colors `: List of base colors used in the fade effect.
         - `collength? `: The number of color transitions between each pair of base colors.
         - `direction? `: The direction of the fade when it is over a text.
        """
        self.colors = colors
        self.collength = collength
        self.direction = direction


    @overload
    def __add__(self, other: Color) -> Fade:
        ...


    @overload
    def __add__(self, other: AnyStringT) -> AnyStringT:
        ...


    def __add__(self, other: AnyStringT | Color) -> AnyStringT | Fade:
        if isinstance(other, str):
            return self.colorate(other) + RESET

        elif isinstance(other, Color):
            return Fade(self.colors + [other])


    def getcolors(self) -> list[Color]:
        """
        Generate a list of interpolated colors based on the colors and collength.

        ### returns
            A list of interpolated colors used in the fade.
        """
        colors: list[Color] = []

        for i in range(len(self.colors) - 1):
            start = self.colors[i]
            end = self.colors[i + 1]

            for j in range(self.collength):
                scale = int((j / self.collength) * 100)
                interpolated_color = start.mix(end, scale)
                colors.append(interpolated_color)

        return colors


    def colorate(self,
                 text: AnyStringT,
                 decal: int = 0) -> AnyStringT:
        """
        Apply the fade effect to a text string with optional starting offset.

        ### arguments
         - `decal`: The starting offset for the fade effect.

        ### returns
            The faded text.
        """
        text = rmansi(text)
        colored_text = ''
        colors = self.getcolors()
        colors += list(reversed(colors))
        colcount = len(colors)

        decal = decal % colcount

        for i in range(decal):
            colors.append(colors[0])
            del colors[0]

        if colcount == 0:
            return text

        match self.direction:
            case 'horizontal':
                for i, char in enumerate(text):
                    color = colors[i % colcount]
                    colored_text += color.ansi + char

            case 'vertical':
                for i, line in enumerate(text.splitlines()):
                    color = colors[i % colcount]
                    colored_text += color.ansi + line + '\n'

        return colored_text



class Col:
    red: ClassVar[Color]
    green: ClassVar[Color]
    blue: ClassVar[Color]
    black: ClassVar[Color]
    white: ClassVar[Color]
    gray: ClassVar[Color]
    grey: ClassVar[Color]
    darkgrey: ClassVar[Color]
    yellow: ClassVar[Color]
    orange: ClassVar[Color]
    purple: ClassVar[Color]
    cyan: ClassVar[Color]
    pink: ClassVar[Color]
    brown: ClassVar[Color]

    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    blue = Color(0, 0, 255)

    black = Color(0, 0, 0)
    white = Color(255, 255, 255)
    gray = grey = black | white
    darkgrey = grey | black

    yellow = Color(255, 255, 0)
    orange = Color(255, 165, 0)
    purple = Color(128, 0, 128)
    cyan = Color(0, 255, 255)
    pink = Color(245, 61, 177)
    brown = Color(165, 42, 42)