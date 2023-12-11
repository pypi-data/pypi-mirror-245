from time import sleep
from sys import stdout
from keyboard import add_hotkey, remove_hotkey
from threading import Event
from typing import ClassVar

from .colors import Color, Fade, Col
from .system import sys
from .ansi import RESET, UNDERLINE


__all__ = ['Icon', 'printd', 'inputd', 'choose', 'yesno', 'underline', 'Icons']



class Icon: # TODO
    symbol: str
    color: Color
    borders: tuple[str, str] | None
    borders_color: Color | None
    
    def __init__(self,
                 symbol: str,
                 color: Color,
                 borders: tuple[str, str] | None = None,
                 borders_color: Color | None = None) -> None:
        self.symbol = symbol
        self.color = color
        self.borders = borders
        self.borders_color = borders_color


    def __str__(self) -> str:
        return self.icon


    def __add__(self, other: str) -> str:
        return self.add(other)


    @property
    def icon(self) -> str:
        if self.borders:
            if self.borders_color:
                lborder = self.borders_color + self.borders[0]
                rborder = self.borders_color + self.borders[1]
            else:
                lborder = self.borders[0]
                rborder = self.borders[1]
        else:
            lborder = rborder = ''
        return lborder + (self.color + self.symbol) + rborder
    
    
    def add(self, text: str) -> str:
        return self.icon + ' ' + text
        



def printd(text: str,
           color: Color | Fade | None = None,
           interval: int | float = 0.05,
           lpadding: int = 0,
           linebreak: bool = True) -> None:
    """
    Prints text with a specified color or fade, and with an interval between each character.

    ### arguments
     - `text`: The text to be printed.
     - `color?`: The color or fade to apply to the text.
     - `interval? `: The time interval between printing each character.
     - `lpadding?`: The left padding margin of the text.
     - `linebreak?`: If True, adds a line break at the end of the printed text.
    """
    stdout.write(' ' * lpadding)
    interval = float(interval)

    if not interval:
        if color:
            stdout.write(color.colorate(text))
        else:
            stdout.write(text)
    else:
        if color:
            if isinstance(color, Color):
                stdout.write(color.ansi)
                for char in text:
                    stdout.write(char)
                    stdout.flush()
                    sleep(interval)

            elif isinstance(color, Fade):
                fade = Fade(color.colors, color.collength, color.direction)
                fadecolors = fade.getcolors()
                fadecolors += list(reversed(fadecolors))
                colcount = len(fadecolors)

                for i, char in enumerate(text):
                    fadecol = fadecolors[i % colcount]
                    stdout.write(fadecol.colorate(char))
                    stdout.flush()
                    sleep(interval)
        else:
            for char in text:
                stdout.write(char)
                stdout.flush()

    if linebreak:
        stdout.write('\n')
    stdout.write(RESET)


def inputd(prompt: str,
           color: Color | Fade,
           resp_color: Color | None = None,
           interval: int | float = 0.05,
           lpadding: int = 0,
           cursor: bool = True) -> str:
    """
    Prompts the user for input with a specified color or fade effect and returns the user's response.

    ### arguments
     - `prompt`: The prompt message to display.
     - `color`: The color or fade for the prompt message.
     - `resp_color?`: The color for the user's response or None for no color.
     - `interval? `: The time interval between printing each character.
     - `lpadding?`: The left padding margin of the text.
     - `cursor?`: If True, displays the cursor during user input.

    ### returns
        The response of the user.
    """
    cursor_state = sys.cursor
    printd(prompt, color, interval, lpadding, False)

    if resp_color:
        stdout.write(resp_color.ansi)

    sys.cursor = cursor
    result = input()
    sys.cursor = cursor_state

    stdout.write(RESET)
    return result


def choose(prompt: str,
           choices: list[str],
           over_color: Color | Fade | None = None,
           lpadding: int = 0) -> int:
    """
    Ask the user to choose one of many choices.

    ### arguments
     - `prompt`: The prompt message to display.
     - `choices`: The choices to display.
     - `over_color?`: The color of the choice that the cursor is on.
     - `lpadding?`: The left padding margin.

    ### returns
        The response of the user exprimed in boolean.
    """
    cursor_state = sys.cursor
    sys.cursor = False

    if not over_color:
        over_color = Fade([(Col.blue | Col.white), (Col.purple | Col.white)], 20)

    lpad = ' ' * lpadding
    choices_lpad = ' ' * (lpadding + 2)

    print(lpad + (Icons.interrogation + prompt))
    choosed = 0
    continu = Event()

    choice_prefix = Col.darkgrey + '[ {} ' + (Col.darkgrey + '] ')

    def up():
        nonlocal choosed
        choosed -= 1
        if choosed < 0:
            choosed = len(choices) - 1
        refresh_choices()

    def down():
        nonlocal choosed
        choosed += 1
        if choosed >= len(choices):
            choosed = 0
        refresh_choices()

    def send():
        nonlocal continu
        continu.set()

    def refresh_choices():
        display_choices('\x1b[1A\x1b[2K' * len(choices))

    def display_choices(initbuffer: str = ''):
        result = initbuffer
        for i, choice in enumerate(choices):
            num = str(i + 1)
            if i == choosed:
                text = choice_prefix.format(over_color + num) + \
                    (over_color + choice) + (Col.darkgrey + ' «')
            else:
                text = choice_prefix.format(RESET + num) + choice

            result += choices_lpad + text + '\n'

        stdout.write(result)

    add_hotkey('up', up)
    add_hotkey('down', down)
    add_hotkey('enter', send)
    display_choices('')

    continu.wait()
    remove_hotkey(up)
    remove_hotkey(down)
    remove_hotkey(send)

    sys.cursor = cursor_state
    return choosed


def yesno(prompt: str,
          over_color: Color | Fade | None = None,
          default: bool = True,
          lpadding: int = 0) -> int:
    """
    Ask the user to choose between yes and no.

    ### arguments
     - `prompt`: The prompt message to display.
     - `over_color?`: The color of the choice that the cursor is on.
     - `default?`: The default choice.
     - `lpadding?`: The left padding margin.

    ### returns
        The index of the item choosen.
    """
    cursor_state = sys.cursor
    sys.cursor = False

    if not over_color:
        over_color = Col.blue | Col.white

    prefix = '\r' + ' ' * lpadding + (Icons.interrogation + prompt) + ' '
    response = default
    continu = Event()

    def display_choice():
        if response:
            yes = over_color + underline('Yes')
            no = 'No'
        else:
            yes = 'Yes'
            no = over_color + underline('No')
        stdout.write(prefix + yes + (Col.gray + ' / ') + no)
        
    def change():
        nonlocal response
        response = not response
        display_choice()

    def send():
        nonlocal continu
        continu.set()

    add_hotkey('left', change)
    add_hotkey('right', change)
    add_hotkey('enter', send)
    display_choice()

    continu.wait()
    remove_hotkey(change)
    remove_hotkey(send)

    stdout.write('\n')
    sys.cursor = cursor_state
    return response


def underline(text: str) -> str:
    """
    Underline a text.

    ### arguments
     - `text`: The text to underline.

    ### returns
        The text underlined.
    """
    return UNDERLINE + text + RESET



class Icons:
    exclamation: ClassVar[Icon]
    interrogation: ClassVar[Icon]

    exclamation = Icon('!', Col.red.mix(Col.white, 30))
    interrogation = Icon('?', Col.blue | Col.white)