# adk info : show project info
import adk.console as console
import adk.glovars as glovars
import adk.errs as errs

from . import conf

def show_project_info(argv: list[list, dict]) -> None:

    if glovars.inited == False:
        errs.NotInited('Your project has not inited yet.')()

    else:
        m = \
f'''
Project Name: {conf.name.get()}
Version: {conf.version.get()}
Create Time: ...
Author(s)...
Description
'''
        console.outl(m)