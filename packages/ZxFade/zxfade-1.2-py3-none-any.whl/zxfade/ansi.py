from typing import LiteralString


__all__ = ['FG_COLOR', 'BG_COLOR', 'RESET',
           'CLEAR', 'TITLE', 'CURSOR',
           'NO_CURSOR', 'UNDERLINE']

FG_COLOR: LiteralString = '\x1b[38;2;{};{};{}m'
"""The ANSI sequence to colorate text with the RGB color value"""
BG_COLOR: LiteralString = '\x1b[48;2;{};{};{}m'
"""The ANSI sequence to colorate the background with the RGB color value"""
RESET: LiteralString = '\x1b[0m'
"""The ANSI sequence to reset all the styles"""
CLEAR: LiteralString = '\x1b[2J\x1b[H'
"""The ANSI sequence to clear all the text before the sequence"""
TITLE: LiteralString = '\x1b]O;{}\a'
"""The ANSI sequence to change the terminal title"""
CURSOR: LiteralString = '\x1b[?25h'
"""The ANSI sequence to activate the terminal cursor"""
NO_CURSOR: LiteralString = '\x1b[?25l'
"""The ANSI sequence to desactivate the terminal cursor"""
UNDERLINE: LiteralString = '\x1b[4m'
"""The ANSI sequence to underline a text"""