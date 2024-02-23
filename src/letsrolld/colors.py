import functools
import sys

import cli_color_py


def colorize(color, text):
    if not sys.stdout.isatty():
        return text
    return color(text)


for color in ('red', 'green', 'blue', 'bold'):
    setattr(sys.modules[__name__], color,
            functools.partial(colorize, getattr(cli_color_py, color)))
