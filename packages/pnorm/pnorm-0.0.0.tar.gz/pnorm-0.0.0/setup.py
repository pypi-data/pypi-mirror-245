# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pnorm']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0',
 'psycopg2-binary>=2.9.9,<3.0.0',
 'pydantic>=2.5.2,<3.0.0',
 'pyyaml>=6.0.1,<7.0.0',
 'rcheck>=0.0.9,<0.0.10']

setup_kwargs = {
    'name': 'pnorm',
    'version': '0.0.0',
    'description': '(Postgres) Not an ORM',
    'long_description': '',
    'author': 'Alex Rudolph',
    'author_email': 'alex3rudolph@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
