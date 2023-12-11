import adk.console as console

def help(argv: list[list, dict]) -> None:
    console.outl(
'''
AtMessger Development Kit v0.0.0

usage:
    adk init    |   init a project in the current dir
    adk uninit
    adk pack
    adk publish
    adk help
    
powered by ...
type /adk help...
''')
    