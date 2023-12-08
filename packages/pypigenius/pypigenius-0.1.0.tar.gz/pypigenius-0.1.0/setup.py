# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypigenius']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypigenius',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'jerry',
    'author_email': 'jerry.zhanghui@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
