from setuptools import setup

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
    classifiers=[],
    dependency_links=[
        'git+git://github.com/unfoldingWord-dev/uw_tools.git#egg=uw_tools',
    ],
    install_requires=[
        'bs4',
        'uw_tools'
    ],
    test_suite='tests'
)
