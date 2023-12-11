import os
import shutil
import json

import adk.console as console
import adk.glovars as glovars

# class struct:pass #namespace struct

if os.path.exists('.atmsg'):
    glovars.inited = True
    
def init(argv: list) -> None:
    if os.path.exists('.atmsg'):
        console.error('this project has already inited.')
        exit() #!
    else:
        os.mkdir('.atmsg')
        os.mkdir('.atmsg/dist')

    meta = dict()
    meta['type'] = console.query('type', console.string, ['plugin', 'texture', 'so on'], 0)
    if meta['type'] == 'plugin':
        meta['end'] = console.query('end', console.string, ['server', 'client'], 0)
        meta['lang'] = console.query('lang', console.string, ['python'], 0)

    with open('.atmsg/meta.json', 'w') as f:
        json.dump(meta, f, indent = 4)

    info = dict()
    info['name'] = console.query('name', console.string)
    info['author'] = console.query('author(s)', console.list)
    info['desc'] = console.query('description', console.string)

    info['version'] = '0.0.0'
    license = ''

    with open('.atmsg/info.json', 'w') as f:
        json.dump(info, f, indent = 4)

    glovars.inited = True
    console.success('Initialization Completed ')

def uninit(argv: list) -> None:
    if not os.path.exists('.atmsg'):
        console.error('this project has not inited yet >_<')
        exit()#!
    imsure = console.confirm('Are you sure to uninit?')
    if imsure: #!
        shutil.rmtree('.atmsg')
        glovars.inited = False
        console.success('Done.')

# def is_inited() api for?