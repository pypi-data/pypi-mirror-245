# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['domainlab',
 'domainlab.algos',
 'domainlab.algos.msels',
 'domainlab.algos.observers',
 'domainlab.algos.trainers',
 'domainlab.algos.trainers.compos',
 'domainlab.compos',
 'domainlab.compos.nn_zoo',
 'domainlab.compos.pcr',
 'domainlab.compos.vae',
 'domainlab.compos.vae.compos',
 'domainlab.dsets',
 'domainlab.exp',
 'domainlab.exp_protocol',
 'domainlab.models',
 'domainlab.tasks',
 'domainlab.utils']

package_data = \
{'': ['*'], 'domainlab': ['uml/*']}

install_requires = \
['gdown>=4.7.1,<5.0.0',
 'matplotlib>=3.6.1,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pillow>=9.3.0,<10.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=13.3.1,<14.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'seaborn==0.12.2',
 'torch>=1.12.0,<2.0.0',
 'torchmetrics>=0.10.0,<0.11.0',
 'torchvision>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'domainlab',
    'version': '0.1.8',
    'description': 'Library of Domain Generalization',
    'long_description': 'None',
    'author': 'Xudong Sun',
    'author_email': 'smilesun.east@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
