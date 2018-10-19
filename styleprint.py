#!/usr/bin/python -i

import warnings

class style:
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

    aliases = dict()

    types = {
        'warning' : ('bold',  'yellow', 'none'),
        'alert'   : ('blink', 'red',    'none'),
        'fail'    : ('roman', 'red',    'none'),
        'okay'    : ('roman', 'green',  'none'),
    }

    end = "\033[0m"

    @staticmethod
    def get_format(**format):

        # Overloadable type
        if format.get('type'):
            type = format.get('type')
            if type not in style.types:
                warnings.warn("Unknown type ignored.")
            else:
                font, color, background_color = style.types[type]

                format.setdefault('f', font)
                format.setdefault('c', color)
                format.setdefault('bc', background_color)


        font = format.get('font') or format.get('f') or 'default'
        color = format.get('color') or format.get('c') or 'default'
        background_color = format.get('backgroundcolor') or \
            format.get('bcolor') or format.get('bc') or 'none'

        warning_msg = "Unknown {el}, defaulting to {default}."
        if font not in style.fonts:
            font = 'roman'
            warnings.warn(warning_msg.format(el="font", default=font))

        if color not in style.colors:
            color = 'gray'
            warnings.warn(warning_msg.format(el="color", default=color))

        if background_color not in style.background_colors:
            background_color = 'none'
            warnings.warn(warning_msg.format(el="background color", default=background_color))

        return (
            style.fonts[font],
            style.colors[color],
            style.background_colors[background_color]
        )

    @staticmethod
    def format(string, **format):
        font, color, background_color = style.get_format(**format)

        return f"\033[{font};{color};{background_color}m{string}{style.end}"

    @staticmethod
    def print(string, end='\n', **format):
        print(style.format(string, **format), end=end)

if "__main__" == __name__:
    style.print("Hello world!", type='alert')
