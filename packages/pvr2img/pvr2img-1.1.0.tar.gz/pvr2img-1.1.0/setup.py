# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['pvr2image']
setup_kwargs = {
    'name': 'pvr2image',
    'version': '1.1.0',
    'description': 'A Python module to easily convert Dreamcast/Naomi .PVR and .PVP files to images + palettes',
    'long_description': '# pvr2image\nA Python module to easily convert Dreamcast/Naomi .PVR and .PVP files to images + palettes\nPlease note it requires Pillow (PIL) module installed\n\n## Installation\n\n```bash\npip3 install pvr2image\n```\n\n ## Credits\n\n- Egregiousguy for YUV420 to YUV420p conversion\n- Kion for VQ handling and logic\n- tvspelsfreak for SR conversion info on Bump to normal map',
    'author': 'VincentNL',
    'author_email': 'zgoro@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VincentNLOBJ/pvr2image',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
