#!/usr/bin/env python3
# termstyles/0.0.1 - Made by N0NL0C4L

import random as _random

class TextStyles(object):
    # Font styles
    default = '\033[0m'
    blink = '\033[5m'
    bold = '\033[1m'
    italic = '\033[3m'
    strikethrough = '\033[9m'
    underlined = '\033[4m'
    overlined = '\033[53m'

class ForeStyles(object):
    # Fore styles
    default = '\033[0m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'

    lightblack = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    lightyellow = '\033[93m'
    lightblue = '\033[94m'
    lightmagenta = '\033[95m'
    lightcyan = '\033[96m'
    lightwhite = '\033[97m'

class BackStyles(object):
    # Back styles
    default = '\033[0m'
    red = '\033[41m'
    green = '\033[42m'
    yellow = '\033[43m'
    blue = '\033[44m'
    magenta = '\033[45m'
    cyan = '\033[46m'
    white = '\033[47m'

    lightblack = '\033[100m'
    lightred = '\033[101m'
    lightgreen = '\033[102m'
    lightyellow = '\033[103m'
    lightblue = '\033[104m'
    lightmagenta = '\033[105m'
    lightcyan = '\033[106m'
    lightwhite = '\033[107m'

# Colorate text
def attach(*text, attr, sep=' ', end='\033[0m'):
    text = sep.join(text)
    return attr + text + end

# Random color
def random(only=(ForeStyles, BackStyles)):	
    therand = []

    if ForeStyles in only:
        fs = ForeStyles()
        while True:
            f_choice = _random.choice(fs.__dir__())
            if f_choice.startswith('__'):
                continue
            else:
                therand.append(getattr(fs, f_choice))
                break

    if BackStyles in only:
        bs = BackStyles()
        while True:
            b_choice = _random.choice(bs.__dir__())
            if b_choice.startswith('__'):
                continue
            else:
                therand.append(getattr(bs, b_choice))
                break

    if Styles in only:
        s = TextStyles()
        while True:
            s_choice = _random.choice(s.__dir__())
            if s_choice.startswith('__'):
                continue
            else:
                therand.append(getattr(s, s_choice))
                break
	

    return _random.choice(therand)

if __name__ == '__main__':
    print(attach('Thank you for using termstyles, Made by N0NL0C4L', attr=ForeStyles.cyan), end='')
    print(ForeStyles.cyan, attach(':)', attr=TextStyles.blink))