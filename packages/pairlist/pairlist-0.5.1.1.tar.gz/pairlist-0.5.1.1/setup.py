# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pairlist']
install_requires = \
['numpy>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'pairlist',
    'version': '0.5.1.1',
    'description': 'Generate neighbor list for the particles in a periodic boundary cell.',
    'long_description': '',
    'author': 'vitroid',
    'author_email': 'vitroid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
