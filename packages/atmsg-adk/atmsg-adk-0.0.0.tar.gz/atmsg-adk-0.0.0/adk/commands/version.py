from . import conf
import adk.console as console

def get(argv: list[list, dict]) -> None:
    v = 'v' + conf.version.get()
    console.outl(v)

def upgrade(argv: list[list, dict]) -> None:
    '''
    usage:
    adk version upgrade patch
    adk version upgrade major
    '''

    if 'h' in argv[1]:
        pass # show help doc

    else:

        at: int

        if len(argv[0]) == 0:
            at = 2
        
        elif argv[0][0] == 'major' or argv[0][0] == '0':
            at = 0

        elif argv[0][0] == 'minor' or argv[0][0] == '1':
            at = 1

        elif argv[0][0] == 'patch' or argv[0][0] == '2':
            at = 2

        else:
            raise

        conf.version.upgrade(at)

        console.success(f'OK. Now i am on {conf.version.get()}')

        

def mapping(argv: list[list, dict]):
    map_ = {
        '': get,
        'get': get,
        'upgrade': upgrade
    }

    subcmd: str
    if len(argv[0]) == 0:
        subcmd = ''
    else:
        subcmd = argv[0].pop(0)
    
    map_[subcmd](argv)