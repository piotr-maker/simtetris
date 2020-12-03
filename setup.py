from setuptools import setup

setup(
    name='simtetris',
    version='1.0',
    url = 'https://github.com/piotr-maker/tetris',
    author='Piotr Włodarski',
    description= 'Simple version of popular russian game tetris', 
    long_description = open('README.md').read(), 
    install_requires = ['pygame>=1.9.6'],
    packages=['simtetris'],
    scripts = ['bin/simtetris'],
)



