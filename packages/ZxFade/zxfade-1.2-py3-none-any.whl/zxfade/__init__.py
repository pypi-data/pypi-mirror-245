from os import system as _system
from importlib.metadata import version

from .system import *
from .colors import *
from .align import *
from .pattern import *
from .animations import *
from .display import *


__all__ = [obj for obj in globals() if not obj.startswith('_')]
__version__ = version(__name__)
__doc__ = """
ZxFade is a Python package to make your programs easy to use and nice to look at.
It contains colors, fades, patterns, animations, system, and more.
by BlueRed.
"""

_system('')