import os
import zipfile

import adk.console as console
from . import conf

def pack(argv: list) -> None:

    home = conf.gethome()
    ver = conf.version.get()

    with zipfile.ZipFile(os.path.join(home, '.atmsg/dist/', ver + '.zip'), 'w') as arch: # allow overwrite?
        for root, dirs, files in os.walk(home):
            rel = os.path.relpath(root, home)
            if rel[0] != '.' or rel == '.':
                for file in files:
                    arch.write(os.path.join(root, file), os.path.join(rel, file))
                    console.log('Add File: ' + os.path.join(root, file))
                if len(files) == 0:
                    arch.write(root, rel)
                    console.log('Add Dir:  ' + root)

        home = os.path.join(home, '.atmsg')
        for root, dirs, files in os.walk(home):
            rel = os.path.join(os.path.relpath(root, home), '.atmsg')
            if rel[0:4] != 'dist' or rel == '.':
                for file in files:
                    arch.write(os.path.join(root, file), os.path.join(rel, file))
                    console.log('Add File: ' + os.path.join(root, file))
                if len(files) == 0:
                    arch.write(root, rel)
                    console.log('Add Dir:  ' + root)

    console.success(f'Generation Completed: v{ver}\x1b[2m <.atmsg/dist/{ver}.zip>\x1b[0m')