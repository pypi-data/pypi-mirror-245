# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepdog', 'deepdog.direct_monte_carlo', 'deepdog.subset_simulation']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.22.3', 'pdme>=0.9.1,<0.10.0', 'scipy==1.10']

setup_kwargs = {
    'name': 'deepdog',
    'version': '0.7.5',
    'description': '',
    'long_description': None,
    'author': 'Deepak Mallubhotla',
    'author_email': 'dmallubhotla+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
