# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rayim']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1,<9.0', 'tqdm>=4.6,<5.0']

entry_points = \
{'console_scripts': ['rayim = rayim:rayim.main']}

setup_kwargs = {
    'name': 'rayim',
    'version': '1.8.0',
    'description': 'Fast image compression for large number of images with Ray library',
    'long_description': '# Ray-Image\n\n🚀 Fast image compression for large number of images with Ray library.\n\n[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.6-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) \n\n## Requirements\n\n- 🐍 [Python>=3.6](https://www.python.org/downloads/)\n- ⚡ [Ray>=1.0.0](https://github.com/ray-project/ray)\n\nTo install `ray`, run\\*:\n```\npip install ray\n```\n\\*For Apple Silicon (M1), follow the instructions [here](https://docs.ray.io/en/latest/ray-overview/installation.html#m1-mac-apple-silicon-support) to install `ray`.\n\n\n## ⬇️ Installation\n\n```\npip install rayim\n```\n\n## ⌨️ Usage\n\n```\nusage: rayim [-h] [-o OUTPUT_DIR] [-q QUALITY] [--overwrite] [-n] [-j]\n             [--replicate-dir-tree] [-s SIZE SIZE] [-d DIV_BY] [-S] [-O]\n             path [path ...]\n\npositional arguments:\n  path                  Path to a single file/directory or multiple\n                        files/directories\n\noptions:\n  -h, --help            show this help message and exit\n  -o OUTPUT_DIR, --output-dir OUTPUT_DIR\n                        Output directory (default: next to original file)\n  -q QUALITY, --quality QUALITY\n                        Output image quality (JPEG only; default: 70)\n  --overwrite           Overwrite the original image\n  -n, --no-subsampling  Turn off subsampling and retain the original image\n                        setting (JPEG only)\n  -j, --to-jpeg         Convert the image(s) to .JPEG\n  --replicate-dir-tree  Replicate the source directory tree in the output\n  -s SIZE SIZE, --size SIZE SIZE\n                        Resize the image to WIDTH HEIGHT\n  -d DIV_BY, --div-by DIV_BY\n                        Divide the image size (WxH) by a factor of n\n  -S, --silent          Silent mode\n  -O, --optimize        Apply default optimization on the image(s)\n  -k, --keep-date       Keep the original creation and modification date\n```\n\n## 📕 Examples\n\n- Running on a single file:\n```shell\nrayim foo.jpg\n# 🚀 foo.jpg: 1157. kB ==> 619.9 kB (-46.4%) | 0.07s\n```\n\n- Running on a folder `foo` and writing the output to `compressed`\n```shell\nrayim foo/ -o compressed\n# (compress_many pid=612778) 🚀 foo.jpg: 988.9 kB ==> 544.8 kB (-44.9%) | 0.08s\n# (compress_many pid=612828) 🚀 bar.jpg: 983.7 kB ==> 541.2 kB (-44.9%) | 0.07s\n# (compress_many pid=612826) 🚀 foobar.jpg: 1001. kB ==> 550.7 kB (-44.9%) | 0.07s\n# (compress_many pid=612786) 🚀 barfoo.jpg: 1001. kB ==> 551.9 kB (-44.8%) | 0.08s\n# ...\n\n# Total:\n#    Before: 1091.32 MB\n#    After: 599.46 MB (-45.0%)\n```\n\n# Speed comparison\n\n### Test 1 (on Apple Silicon M1, 8-cores)\n\n| Method      | Number of files | Speed |\n| ----------- | ----------- | ----------- | \n| Regular compression      | 1,000       | `60.090s` | \n| rayim   | 1,000        | **`26.937s`** (**`55.17%`** faster) | \n\n```YAML\nTotal:\n    Before: 1091.32 MB\n    After: 599.46 MB (-45.0%)\n```\n\n### Test 2 (on Intel @ 2.299GHz, 32-cores)\n\n| Method      | Number of files | Speed |\n| ----------- | ----------- | ----------- |\n| Regular compression      | 6,000       | `7m42.919s` |\n| rayim   | 6,000        | **`5m15.423s`** (**`31.96%`** faster) | \n\n```YAML\nTotal:\n    Before: 6040.59 MB\n    After: 3321.70 MB (-45.0%)\n```\n',
    'author': 'Mohammad Alyetama',
    'author_email': 'malyetama@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
