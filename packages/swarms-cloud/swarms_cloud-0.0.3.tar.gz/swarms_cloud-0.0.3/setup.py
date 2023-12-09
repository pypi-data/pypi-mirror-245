# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarms_cloud']

package_data = \
{'': ['*']}

install_requires = \
['fastapi', 'skypilot', 'supabase', 'swarms']

setup_kwargs = {
    'name': 'swarms-cloud',
    'version': '0.0.3',
    'description': 'Swarms Cloud - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Swarms Cloud\nDeploy your autonomous agents to the cloud with infinite scalability, 99% uptime, and a polymorphic api.\n\n\nBase swarms code -> fastapi code is added to top and bottom -> agent is decorated with expose as api decorator -> file is parsed and then -> added onto yaml for -> skypilot\n\n\n# Install\n`pip install swarms-cloud`\n\n\n# Stack\n- Backend: FastAPI\n- Skypilot for container management\n- Stripe for payment tracking\n- Postresql for database\n\n\n\n# License\nMIT',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarms-cloud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
