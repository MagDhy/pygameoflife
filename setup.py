from setuptools import setup

setup(
    name='pygameoflife',
    version='1.0.0',
    description='Conway\'s Game of Life implements with PyGame',
    url='https://github.com/MagDhy/pygameoflife',
    author='MagDhyn',
    author_email='magalidhyne@live.be',
    license='GPL-3.0',
    packages=['pygameoflife'],
    scripts=[
        'bin/pygameoflife',
        'bin/pygameoflife.bat'
    ],
    zip_safe=False,
    install_requires=[
        'pygame'
    ]
)