# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gemmap']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79',
 'cobra>=0.26',
 'pandas>=1.5',
 'pyvis>=0.3',
 'requests>=2.28']

setup_kwargs = {
    'name': 'gemmap',
    'version': '0.1.1',
    'description': '',
    'long_description': '# gemmap',
    'author': 'Gioele Lazzari',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
