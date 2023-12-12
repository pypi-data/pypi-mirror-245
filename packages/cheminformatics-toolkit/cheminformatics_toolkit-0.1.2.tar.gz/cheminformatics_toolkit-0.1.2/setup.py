# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cheminformatics_toolkit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cheminformatics-toolkit',
    'version': '0.1.2',
    'description': '',
    'long_description': '# About\n\n# Documentation\n\n# Setup\n\n# Testing\n\n# Quick start\n\n# Authors\n\n# Contributing\n',
    'author': 'gosia olejniczak',
    'author_email': 'gosia.olejniczak@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
