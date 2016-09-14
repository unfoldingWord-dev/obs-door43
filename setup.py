import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name)).read()


setup(
    name="obs_door43",
    version="0.0.1",
    author="unfoldingWord",
    author_email="phillip_hopper@wycliffeassociates.org",
    description="A Python script that takes OBS files in HTML format and applies the Door43 template",
    license="MIT",
    keywords="unfoldingWord OBS Door43",
    url="https://github.org/unfoldingWord-dev/obs_door43",
    packages=['obs_door43'],
    long_description=read('README.md'),
    classifiers=[],
    dependency_links=[
        'git+git://github.com/unfoldingWord-dev/uw_tools.git#egg=uw_tools',
    ],
    install_requires=[
        'bs4',
        'uw_tools'
    ]
)
