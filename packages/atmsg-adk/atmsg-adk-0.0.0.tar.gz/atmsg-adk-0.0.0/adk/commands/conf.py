import json
import os
from threading import Thread as thread
import adk.glovars as glovars
import adk.console as console

info: dict

def _read() -> None:

    global info
    if glovars.inited:
        if 'info' not in dir():
            with open('.atmsg/info.json') as f:
                info = json.load(f)
    else:
        console.error('has not inited.')
        exit()


def _flush():
    with open('.atmsg/info.json', 'w') as f:
        json.dump(info, f)

def gethome() -> str:
    return os.getcwd()

class version: # ver history

    def get() -> str:
        _read() #!
        return info['version']
    
    def set(version: str) -> None:
        info['version'] = version
        _flush()

    def upgrade(at: int) -> None:
        _read() #!
        v = version.get().split('.')
        for i in range(len(v)):
            v[i] = int(v[i])
        
        if at == 2:
            v[2] += 1
        elif at == 1:
            v[1] += 1
            v[2] = 0
        elif at == 0:
            v[0] += 1
            v[1] = 0
            v[2] = 0

        r = str()
        for i in v:
            r += str(i) + '.'
        r = r[:-1]
        version.set(r)


class name:

    def get() -> str:
        _read()
        return info['name']
    
    def set(newname: str) -> None:
        _read()
        info['name'] = newname
        _flush()

