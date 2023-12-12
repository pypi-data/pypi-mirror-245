# pip-dep-bump
[![Python 3.11+](https://upload.wikimedia.org/wikipedia/commons/6/62/Blue_Python_3.11%2B_Shield_Badge.svg)](https://www.python.org)
[![License: GPL v3](https://upload.wikimedia.org/wikipedia/commons/8/86/GPL_v3_Blue_Badge.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

Bumps requirements.txt deps and updates them in the current virtualenv

## Installation
```bash
pip install pip-dep-bump
```

Also installs a CLI alias called `pdb` which can be used to invoke the program directly

## Usage
```
usage: __main__.py [-h] [-r requirements.txt] [-d]

pip-dep-bump CLI

options:
  -h, --help           show this help message and exit
  -r requirements.txt  The requirements.txt file to work off of. Default is ./requirements.txt
  -d                   Dry run, print contents of new requriements.txt
```