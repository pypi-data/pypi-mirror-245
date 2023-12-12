# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teragpt']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'local-attention', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'teragpt',
    'version': '0.0.1',
    'description': 'Paper - Pytorch',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# TeraGPT\nTrain a production grade GPT in less than 400 lines of code. Better than Karpathy's verison and GIGAGPT\n\n\n\n## Install\n`pip3 install  `\n\n\n\n## Usage\n```python\nimport torch\nfrom teragpt.main import TeraGPT\n\nmodel = TeraGPT(\n    dim=4096,\n    depth=6,\n    heads=8,\n    num_tokens=20000,\n)\n\nx = torch.randint(0, 20000, (1, 4096))\n\nout = model(x)\nprint(out.shape)\n\n```\n\n\n# License\nMIT\n\n\n\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/TeraGPT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
