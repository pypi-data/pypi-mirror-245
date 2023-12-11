from setuptools import setup

DESCRIPTION = "My personal Advent of Code helper functions."

VERSION = '0.0.6'

setup(
    name="flatypus-aochelpers",
    version=VERSION,
    author="Hinson Chan",
    author_email="<yhc3141@gmail.com>",
    maintainer="Hinson Chan",
    maintainer_email="<yhc3141@gmail.com>",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=['aochelpers'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    license='MIT'
)
