import setuptools

desc: str
with open('README.md') as f:
    desc = f.read()

print(setuptools.find_packages())
setuptools.setup(
    name = 'atmsg-adk', # id / name
    version = '0.0.0',
    author = 'Cure-X',
    description = 'A Command-Line Development Manager For AtMessager', # full name?
    long_description = desc,
    # long_description_content_type = 
    # entry_points = {
    #     'console-scripts': [
    #         'adk=adk'
    #     ]
    # },
    
    scripts = ['sh/adk'],

    author_email = 'admin@cure-x.net',
    py_modules = [],
    packages = setuptools.find_packages()
    
    # packages = 
    
)