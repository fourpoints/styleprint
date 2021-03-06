#!/usr/bin/python -i

import sys
import warnings

class Encoding:
    fonts = {
        'roman'         : 0,
        'bold'          : 1,
        'italic'        : 3,
        'underline'     : 4,
        'blink'         : 5,
        'mark'          : 7,
        'strikethrough' : 9,
        'default'       : 0,
    }

    colors = {
        'black'       : 30,
        'darkred'     : 31,
        'darkgreen'   : 32,
        'darkyellow'  : 33,
        'blue'        : 34,
        'darkmagenta' : 35,
        'darkcyan'    : 36,
        'lightgrey'   : 37, 'lightgray' : 37,
        'grey'        : 38, 'gray'      : 38,
        'darkgrey'    : 90, 'darkgray'  : 90,
        'red'         : 91,
        'green'       : 92,
        'yellow'      : 93,
        'violet'      : 94,
        'magenta'     : 95,
        'cyan'        : 96,
        'white'       : 97,
        'default'     : 38,
    }

    background_colors = {
        'none'    : 40,
        'black'   : 40,
        'red'     : 41,
        'green'   : 42,
        'yellow'  : 43,
        'blue'    : 44,
        'magenta' : 45,
        'cyan'    : 46,
        'white'   : 47,
    }

    global_aliases = {
        'r' : 'red',
        'g' : 'green',
        'b' : 'blue',
        'k' : 'black',
        'c' : 'cyan',
        'm' : 'magenta',
        'y' : 'yellow',
        'w' : 'white',
    }

    types = {
        'warning' : ('bold',  'yellow', 'none'),
        'alert'   : ('blink', 'red',    'none'),
        'error'   : ('roman', 'red',    'none'),
        'fail'    : ('roman', 'red',    'none'),
        'okay'    : ('roman', 'green',  'none'),
        'success' : ('roman', 'green',  'none'),
    }

    end = "\033[0m"

    @staticmethod
    def get_format(**format):
        # Get aliases
        for key, value in format.items():
            if value in Encoding.global_aliases:
                format[key] = Encoding.global_aliases[value]

        # Overloadable type
        if format.get('type'):
            type = format.get('type')
            if type not in Encoding.types:
                warnings.warn("Unknown type ignored.")
            else:
                font, color, background_color = Encoding.types[type]

                # setdefault can be overloaded
                format.setdefault('f', font)
                format.setdefault('c', color)
                format.setdefault('bc', background_color)


        font = format.get('font') or format.get('f') or 'default'
        color = format.get('color') or format.get('c') or 'default'
        background_color = format.get('backgroundcolor') or \
            format.get('bgcolor') or format.get('bgc') or \
            format.get('bcolor') or format.get('bc') or 'none'

        # Default font if non-existing key
        warning_msg = "Unknown {el}, defaulting to {default}."
        if font not in Encoding.fonts:
            font = 'roman'
            warnings.warn(warning_msg.format(el="font", default=font))

        if color not in Encoding.colors:
            color = 'gray'
            warnings.warn(warning_msg.format(el="color", default=color))

        if background_color not in Encoding.background_colors:
            background_color = 'none'
            warnings.warn(warning_msg.format(el="background color", default=background_color))

        # Return encodings
        return (
            Encoding.fonts[font],
            Encoding.colors[color],
            Encoding.background_colors[background_color]
        )

def register_alias(**aliases):
    """
    Registers a new alias.

    Input should be of the form:
    alias_name = key_name

    Example:
    register_alias(rouge = "red")

    Note: aliases are shared between colors, bgcolors, fonts & types.
    """
    Encoding.global_aliases.update(aliases)

def register_type(**types):
    """
    Registers a new type.

    Input should be of the form:
    type_name = ("font", "color", "background color")


    Example:
    register_alias(cool = ("roman", "blue", "red")
    """
    Encoding.types.update(types)

def sformat(string, **format) -> str:
    """
    Formats the string.

    Example:
    sformat("Hello world!", color="red", font="italic")

    This is styleprint or sprint. It allows for simple stylized text in unix consoles.

    == Functions ==
    sprint(string, end='\\n', **format)  --  prints formatted text
    sformat(string, **format)           --  formats text
    register_type(**types)              --  registers new type
    register_alias(**aliases)           --  registers new alias

    == Formatting ==
    The **format argument accepts the following keyword and values

    Parameters
    ----------
    font, f : str
        Font keyword, used to define the font style.

        Values:
            - roman
            - bold
            - italic
            - underline
            - blink
            - mark
            - strikethrough
            - default (roman)

    - color, c : str
        Color keyword, used to define the text-color.


        Values:
            - black, k
            - darkred
            - darkgreen
            - darkyellow
            - blue, b
            - darkmagenta
            - darkcyan
            - lightgrey, lightgray
            - grey, gray
            - darkgrey, darkgray
            - red, r
            - green, g
            - yellow, y
            - violet
            - magenta, m
            - cyan, c
            - white, w
            - default (gray-ish)


    backgroundcolor, bgcolor, bgc, bcolor, bc : str
        The background color keyword, used to define text-highlighting..

        Values:
            - black, k
            - red, r
            - green, g
            - yellow, y
            - blue, b
            - magenta, m
            - cyan, c
            - white, w


    type : str
        The type argument, used to apply predefined styles (combinations)

        Valid keywords (by default)
                        font    color     background color
            - warning | bold    yellow    none
            - alert   | blink   red       none
            - fail    | roman   red       none
            - okay    | roman   green     none


    Returns
    -------
    : None
    """
    font, color, background_color = Encoding.get_format(**format)

    return f"\033[{font};{color};{background_color}m{string}{Encoding.end}"

def sprint(*stringable, sep=' ', end='\n', file=sys.stdout, flush=False, **format) -> None:
    """
    Prints a formatted string.

    Input should be of the form:
    "string_to_format", end (optional), **format

    Example:
    sprint("Hello world!", bgcolor="yellow", font="blink")

    Parameters
    ----------
    *stringable : objects w/ __str__ method
        A string or objects that should be printed

    sep : str = ' '
        A separator string to join stringable.

    end : str = '\n'
        A string to be appended to the stringable.

    file : object w/ write(str) method = sys.stdout
        The place where the stringable will be printed. (Defaults to terminal.)

    flush : bool
        Determines whether or not the stream is forcibly flushed.

    **format : {kw : str}
        See help(styleprint.sformat)

    Returns
    -------
    : None
    """

    print(sformat(sep.join(map(str, stringable)), **format), end=end, file=sys.stdout, flush=False)

if "__main__" == __name__:
    sprint("Hello world!", type="alert")
    sprint("Hello moon!", color="w", bcolor="red", font="italic")
