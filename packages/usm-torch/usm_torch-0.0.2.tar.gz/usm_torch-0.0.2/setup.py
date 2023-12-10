# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usm_torch']

package_data = \
{'': ['*']}

install_requires = \
['pytest', 'torch', 'torchaudio']

setup_kwargs = {
    'name': 'usm-torch',
    'version': '0.0.2',
    'description': 'usm - Pytorch',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# USM\nImplementation of Google's universal speech model called USM\n\n\n# Install\n`pip `\n\n# License\nMIT\n\n\n\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/USM',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
