'''
example
adk init type=python-plugin
type: plugin
end: client
lang: python
adk pack
adk version update-to
adk source add plugin.atmsg.org
adk publish
'''

'''
adk =h
adk =v
'''

'''
adk clone ...
'''

import adk.console as console
packname = console.query('package name', console.string) # non-wb-string
print(packname)

yn = console.query('Yes OR No', console.string, ['y', 'n'], 0)
print(yn)