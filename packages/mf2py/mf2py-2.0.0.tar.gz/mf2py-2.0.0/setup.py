# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mf2py']

package_data = \
{'': ['*'], 'mf2py': ['backcompat-rules/*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'html5lib>=1.1,<2.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'mf2py',
    'version': '2.0.0',
    'description': 'Microformats parser',
    'long_description': 'None',
    'author': 'Tom Morris',
    'author_email': 'tom@tommorris.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
