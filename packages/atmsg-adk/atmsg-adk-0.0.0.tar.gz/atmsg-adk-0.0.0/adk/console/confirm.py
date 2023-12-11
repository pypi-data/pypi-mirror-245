from .query import query
import adk.console as console

def confirm(info: str, default: int = None) -> bool:
    if default == None:
        foo = '[y, n]'
    elif default == True:
        foo = '[\x1b[1;36my\x1b[0m, n]'
    else:
        foo = '[y, \x1b[1;36mn\x1b[0m]'

    ans: str = input(info + ' \x1b[2m => \x1b[0m ' + foo + ' = ')
    ans = ans.lower()
    if ans == 'y' or ans == 'yes':
        return True
    elif ans == 'n' or ans == 'no':
        return False
    else:
        console.warning('must be one of y, yes, n, no, ignore case')
        confirm(info, default)