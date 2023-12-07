from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Utils for the PokéApp'
LONG_DESCRIPTION = 'All subfunctions, lists and dicts needed in the main.py are included here'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="PokeAppUtils", 
        version=VERSION,
        author="Ingo Kognito",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'PokeAppUtils'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)