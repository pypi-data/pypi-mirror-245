import re
from . import datatypes
import adk.console as console

def query(name: str, type: datatypes.type, options = [], default: int = None): # *args?

    #json

    prompt = str()
    prompt += name

    if type != datatypes.auto:
        prompt += '\x1b[2m -> \x1b[0m\x1b[1;36m'
        prompt += type.name
        prompt += '\x1b[0m'

    if len(options) != 0:
        prompt += '\x1b[2m => \x1b[0m[' # italic nice beautiful font
        for i in range(len(options)):
            if default != None and i == default:
                prompt += '\x1b[4m\x1b[1;36m'
                prompt += str(options[i])
                prompt += '\x1b[0m'
            else:
                prompt += str(options[i])
            prompt += ', '
        prompt = prompt[:-2]
        prompt += '\x1b[0m]'
    prompt += ' = '

    result = input(prompt).strip(' ')
    # result = re.sub('\\s+', ' ', result) #!
    if len(options) != 0:
        if result == '':
            if default != -1:
                result = options[default]
                print('\x1b[4m' + options[default] + '\x1b[\0m')
            else:
                console.warning('... not in [], try again.')
                result = query(name, type, options, default)
        else:
            if result not in options:
                console.warning('... not in [], try again.')
                result = query(name, type, options, default)

    return result
