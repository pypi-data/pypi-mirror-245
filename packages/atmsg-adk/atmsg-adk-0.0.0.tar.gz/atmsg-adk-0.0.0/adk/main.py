import adk.commands as commands

def mapping(argv: list[list, dict]):
    map_ = {
        '': commands.help,
        'help': commands.help,

        'init': commands.init,
        'uninit': commands.uninit,
        'pack': commands.pack,

        'ver': commands.version.mapping,
        'version': commands.version.mapping,

        'info': commands.show_project_info
        }
    
    subcmd: str
    if len(argv[0]) == 0:
        subcmd = ''
    else:
        subcmd = argv[0].pop(0)
    
    map_[subcmd](argv)

# project name not null
# cmd ignore case
# adk =v =h