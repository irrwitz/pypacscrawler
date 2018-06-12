from setuptools import setup

setup(
    name="pypacscrawler",
    version='0.0.4',
    pymodules=['run'],
    install_requires=[
        'pandas',
        'click'
    ],
    entry_points='''
        [console_scripts]
        pypacscrawler=run:cli
    ''',
)
