"""
Setup file for mathemagician to allow installation and access via pip.
"""

from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    install_requires = file.read().splitlines()

setup(
    name='mathemagician',
    version='0.0.0',
    description='A command-line RPG game based on maths, puzzles and coding.',
    long_description=long_description,
    url='https://github.com/peter-hunt/mathemagician',
    author='PeterHunt',
    author_email='huangtianhao@icloud.com',
    license='MIT',
    python_requires='>=3.12',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent ',
        'Programming Language :: Python :: 3.12',
        'Topic :: Education',
        'Topic :: Games/Entertainment :: Role-Playing',
        'Topic :: Scientific/Engineering',
        'Topic :: Terminals',
    ],
    install_requires=install_requires,
)
